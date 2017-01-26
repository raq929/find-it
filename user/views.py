from django.conf import settings

# contrib
from django.contrib.auth import get_user, get_user_model, logout
from django.contrib.auth.decorators import \
  login_required
from django.contrib.auth.tokens import \
  default_token_generator as token_generator
from django.contrib.messages import error, success

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.template.response import \
  TemplateResponse

# utils
from django.utils.decorators import \
  method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

#views
from django.views.decorators.cache import \
  never_cache
from django.views.decorators.csrf import \
  csrf_protect
from django.views.decorators.debug import \
  sensitive_post_parameters
from django.views.generic import DetailView, View

from guardian.shortcuts import assign_perm, get_objects_for_user
from guardian.mixins import PermissionRequiredMixin

from .decorators import class_login_required
from .forms import (AddHouseResidentForm, AddHouseVisitorForm,
                    ResendActivationEmailForm, UserCreationForm)
from item.models import House
from .models import Profile
from .utils import (AddUserDoneMixin, AddUserMixin, MailContextViewMixin,
                    ProfileGetObjectMixin, ProfileHouseContextMixin,
                    SendMailMixin)
from item.models import House

class DisableAccount(View):
  success_url = settings.LOGIN_REDIRECT_URL
  template_name = 'user/user_confirm_delete.html'


  @method_decorator(csrf_protect)
  @method_decorator(login_required)
  def get(self, request):
    return TemplateResponse(
      request,
      self.template_name)

  @method_decorator(csrf_protect)
  @method_decorator(login_required)
  def post(self, request):
    user = get_user(request)
    user.set_unusable_password()
    user.is_active = False
    user.save()
    logout(request)

    return redirect(self.success_url)

@class_login_required
class AddResident(PermissionRequiredMixin, AddUserMixin, SendMailMixin,
                  DetailView):
    email_template_name = 'user/add_resident_email.txt'
    form_class = AddHouseResidentForm
    model = House
    permission_required = ['change_house']
    raise_exception = True
    slug_url_kwarg = 'house_slug'
    subject_template_name = 'user/add_resident.txt'
    success_url = 'dj-auth:add_resident_done'
    template_name = 'user/add_resident_form.html'


@class_login_required
class AddVisitor(PermissionRequiredMixin, AddUserMixin, SendMailMixin,
                 DetailView):
    email_template_name = 'user/add_visitor_email.txt'
    form_class = AddHouseVisitorForm
    model = House
    permission_required = ['change_house']
    raise_exception = True
    slug_url_kwarg = 'house_slug'
    subject_template_name = 'user/add_visitor.txt'
    success_url = 'dj-auth:add_visitor_done'
    template_name = 'user/add_visitor_form.html'


@class_login_required
class AddResidentDone(AddUserDoneMixin, View):
  template_name = 'user/add_user_done.html'
  type_of_user = 'resident'


@class_login_required
class AddVisitorDone(AddUserDoneMixin, View):
  template_name = 'user/add_user_done.html'
  type_of_user = 'visitor'


class CreateAccount(MailContextViewMixin, View):
  form_class = UserCreationForm
  success_url = reverse_lazy('dj-auth:create_done')
  template_name = 'user/user_create.html'

  @method_decorator(csrf_protect)
  def get(self, request):
    return TemplateResponse(
      request,
      self.template_name,
      { 'form': self.form_class() })

  @method_decorator(csrf_protect)
  @method_decorator(sensitive_post_parameters(
    'password1', 'password2'))
  def post(self, request):
    bound_form = self.form_class(request.POST)
    if bound_form.is_valid():
      # not catching returned user
      bound_form.save(
        **self.get_save_kwargs(request))
      if bound_form.mail_sent: # email sent?
        return redirect(self.success_url)
      else:
        errs = (
          bound_form.non_field_errors())
        for err in errs:
          error(request, err)
        redirect('dj-auth:resend_activation')

    return TemplateResponse(
      request,
      self.template_name,
      { 'form': bound_form })


class ActivateAccount(View):
  success_url = reverse_lazy('dj-auth:login')
  template_name = 'user/user_activate.html'

  @method_decorator(never_cache)
  def get(self, request, uidb64, token):
    User = get_user_model()
    try:
      uid = force_text(
        urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
    except (TypeError, ValueError,
      OverflowError, User.DoesNotExist):
      user = None
    if (user is not None
          and token_generator
          .check_token(user, token)):
      user.is_active = True
      user.save()
      success(
        request,
        'User Activated! '
        'You may now log in.')
      return redirect(self.success_url)
    else:
      return TemplateResponse(
        request,
        self.template_name)

@class_login_required
class ActivateAddResident(View):
  success_url = reverse_lazy('dj-auth:profile')
  template_name = 'user/user_activate_add_resident.html'
  @method_decorator(never_cache)
  def get(self, request, uidb64, hidb64, token):
    User = get_user_model()
    try:
      uid = force_text(
        urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
    except (TypeError, ValueError,
      OverflowError, User.DoesNotExist):
      user = None

    try:
      hid = force_text(
        urlsafe_base64_decode(hidb64))
      house = House.objects.get(pk=hid)
    except (TypeError, ValueError,
      OverflowError, House.DoesNotExist):
      house = None

    if (user is not None
          and house is not None
          and token_generator
          .check_token(user, token)):

      assign_perm('is_resident', user, house)
      assign_perm('view_house', user, house)

      success(
        request,
        'You have been added as a resident of {} house.'.format(house.name))
      return redirect(self.success_url)
    else:
      return TemplateResponse(
        request,
        self.template_name,
        { 'house': house })


@class_login_required
class ActivateAddVisitor(View):
    success_url = reverse_lazy('dj-auth:profile')
    template_name = 'user/user_activate_add_visitor.html'

    @method_decorator(never_cache)
    def get(self, request, uidb64, hidb64, token):
        User = get_user_model()
        try:
            uid = force_text(
              urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError,
                OverflowError, User.DoesNotExist):
            user = None

        try:
            hid = force_text(
              urlsafe_base64_decode(hidb64))
            house = House.objects.get(pk=hid)
        except (TypeError, ValueError,
                OverflowError, House.DoesNotExist):
            house = None

        if (user is not None
            and house is not None
            and token_generator
                .check_token(user, token)):

            assign_perm('view_house', user, house)

            success(
              request,
              'You have been added as a visitor of {} house.'
              .format(house.name))
            return redirect(self.success_url)
        else:
            return TemplateResponse(
              request,
              self.template_name,
              { 'house': house })

@class_login_required
class ProfileDetail(
  ProfileGetObjectMixin, ProfileHouseContextMixin, DetailView):
    model = Profile

    def get(self, request):
        can_view = get_objects_for_user(request.user, 'item.view_house')
        resident_of = get_objects_for_user(
          request.user, 'item.is_resident')

        self.houses = request.user.profile.houses.all()
        # find all the houses that user has view permission but
        # is not a resident of
        self.can_view = set(can_view).difference(set(resident_of))
        # find all houses that user is a resident but not an owner of
        self.resident_of = set(resident_of).difference(set(self.houses))

        return super().get(request)


class ResendActivationEmail(
  MailContextViewMixin, View):
  form_class = ResendActivationEmailForm
  success_url = reverse_lazy('dj-auth:login')
  template_name = 'user/resend_activation.html'

  @method_decorator(csrf_protect)
  def get(self, request):
    return TemplateResponse(
      request,
      self.template_name,
      { 'form': self.form_class() })

  @method_decorator(csrf_protect)
  def post(self, request):
    bound_form = self.form_class(request.POST)
    if bound_form.is_valid():
      user = bound_form.save(
        **self.get_save_kwargs(request))
      # if it's a valid user, show the error
      if(user is not None
          and not bound_form.mail_sent):
        for err in errs:
          error(request, err)
        if errs:
          bound_form.errors.pop('__all__')
        # send the user to the Resend email form
        return TemplateResponse(
          request,
          self.template_name,
          { 'form': bound_form })
    # if it's not a valid user, pretend success
    success(request,
      'Activation Email Sent!')
    return redirect(self.success_url)
