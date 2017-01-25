import logging
import traceback
from smtplib import SMTPException
from logging import CRITICAL, ERROR
from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.tokens import \
  default_token_generator as token_generator
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import (
    BadHeaderError, send_mail)
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import \
  render_to_string
from django.template.response import \
  TemplateResponse
from django.utils.encoding import force_bytes
from django.utils.http import \
  urlsafe_base64_encode
from item.models import House

logger = logging.getLogger(__name__)


class ActivationMailFormMixin:
  mail_validation_error = ''

  @property
  def mail_sent(self):
    if hasattr(self, '_mail_sent'):
      return self._mail_sent
    return False

  def log_mail_error(self, **kwargs):
    msg_list = [
      'Activation email did not send. \n',
      'from_email: {from_email}\n'
      'subject: {subject}\n'
      'message: {message}\n'
    ]
    recipient_list = kwargs.get('recipient_list', [])
    for recipient in recipient_list:
      msg_list.insert(
        1, 'recipient: {r}\n'.format(
          r=recipient))
    if 'error' in kwargs:
      level = ERROR
      error_msg = (
        'error: {0.__class__.__name__}\n'
        'args: {0.args}\n')
      error_info = error_msg.format(
        kwargs['error'])
      msg_list.insert(1, error_info)
    else:
      level = CRITICAL

    msg = ''.join(msg_list).format(**kwargs)
    logger.log(level, msg)

  @mail_sent.setter
  def set_mail_sent(self, value):
    raise TypeError(
      'Cannot set mail_sent attribute')

  def get_message(self, **kwargs):
    email_template_name = kwargs.get(
      'email_template_name')
    context = kwargs.get('context')
    return render_to_string(email_template_name, context)

  def get_subject(self, **kwargs):
    subject_template_name = kwargs.get(
      'subject_template_name')
    context = kwargs.get('context')
    subject = render_to_string(
      subject_template_name, context)
    # subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    return subject

  def get_context_data(
      self, request, user, house, context=None):
    if context is None:
      context = dict()
    current_site = get_current_site(request)
    if request.is_secure():
      protocol = 'https'
    else:
      protocol = 'http'
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    hid = urlsafe_base64_encode(force_bytes(house.pk))
    context.update({
        'domain': current_site.domain,
        'protocol': protocol,
        'site_name': current_site.name,
        'token': token,
        'uid': uid,
        'user': user,
        'house': house,
        'hid': hid
      })
    return context

  def _send_mail(self, request, user, house, **kwargs):
    kwargs['context'] = self.get_context_data(
      request, user, house)
    mail_kwargs = {
      "subject": self.get_subject(**kwargs),
      "message": self.get_message(**kwargs),
      "from_email": settings.DEFAULT_FORM_EMAIL,
      "recipient_list": [user.email]
    }
    try:
      #number_sent will be 1 or 0
      number_sent = send_mail(**mail_kwargs)
    except Exception as error:
      self.log_mail_error(
        error=error, **mail_kwargs)
      if isinstance(error, BadHeaderError):
        err_code = 'badheader'
      elif isinstance(error, SMTPException):
        err_code = 'smtperror'
      else:
        err_code = 'unexpectederror'
      return(False, err_code)
    else:
      if number_sent > 0:
        return(True, None)
    self.log_mail_error(**mail_kwargs)
    return (False, 'unknownerror')

  def send_mail(self, user, **kwargs):
    request = kwargs.pop('request', None)
    house = kwargs.pop('house', None)
    if request is None:
      tb = traceback.format.stack()
      tb = [' ' + line for line in tb]
      logger.warning(
        'send_mail called without '
        'request. \nTraceback:\n{}'.format(
          ''.join(tb)))
      self._mail_sent = False
      return self.mail_sent
    self._mail_sent, error = (
      self._send_mail(
        request, user, house, **kwargs))
    if not self.mail_sent:
      self.add_error(
        None, # no field - form error
        ValidationError(
          self.mail_validation_error,
          code=error))
    return self.mail_sent

class MailContextViewMixin:
  email_template_name = 'user/email_create.txt'
  subject_template_name = 'user/subject_create.txt'

  def get_save_kwargs(self, request):
    return {
      'email_template_name':
        self.email_template_name,
      'request': request,
      'subject_template_name':
        self.subject_template_name,
    }


class SendMailMixin:

    def get_save_kwargs(self, request):
        return {
          'email_template_name': self.email_template_name,
          'request': request,
          'subject_template_name': self.subject_template_name
        }


class ProfileGetObjectMixin:

  def get_object(self, queryset=None):
    current_user = get_user(self.request)
    return current_user.profile

class ProfileHouseContextMixin:
  def get_context_data(self, **kwargs):
    context = {}
    if hasattr(self, 'resident_of'):
      context = {
        'resident_of':
            self.resident_of,
      }

    context.update(kwargs)
    return super().get_context_data(**context)

class AddUserDoneMixin:

    def get(self, request, **kwargs):
        house_slug = kwargs.get('house_slug')
        house = get_object_or_404(House,
                                  slug__iexact=house_slug)

        return TemplateResponse(
          request,
          self.template_name,
          {
            'house': house,
            'type_of_user': self.type_of_user,
           })


class AddUserMixin:

    def get(self, request, **kwargs):
        house_slug = kwargs.get('house_slug')
        house = get_object_or_404(House,
                                  slug__iexact=house_slug)

        return TemplateResponse(
          request,
          self.template_name,
          { 'form': self.form_class(),
            'house': house,
           })

    def post(self, request, **kwargs):
        bound_form = self.form_class(request.POST)
        house_slug = kwargs.get('house_slug')
        house = get_object_or_404(House,
                                  slug__iexact=house_slug)

        success_url = reverse_lazy(self.success_url,
                                   kwargs={ 'house_slug': house_slug })

        if bound_form.is_valid():
            bound_form.save(
              **self.get_save_kwargs(request),
              house=house)
            if bound_form.mail_sent:
                return redirect(success_url)
            else:
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                redirect('dj-auth:profile')

        return TemplateResponse(
          request,
          self.template_name,
          { 'form': bound_form,
            'house': house })
