from django.db.models import Model
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

class DetailView(View):
  context_object_name = ''
  model = None
  template_name = ''
  template_name_suffix = '_detail'

  def get(self, request, **kwargs):
    self.kwargs = kwargs
    self.object = self.get_object()
    template_name = self.get_template_names()
    context = self.get_context_data()

    return render(
      request,
      template_name,
      context)

  def get_context_data(self):
    context = {}
    if self.object:
      context_object_name = (
        self.get_context_object_name())
      if context_object_name:
        context[context_object_name] = (
          self.object)
    return context


  def get_context_object_name(self):
    if self.context_object_name:
      return self.context_object_name
    elif isinstance(self.object, Model):
      return self.object._meta.model_name
    else:
      return None

  def get_template_names(self):
    if self.template_name:
      return self.template_name
    return "{app}/{model}{suffix}.html".format(
      app=self.object._meta.app_label,
      model=self.object._meta.model_name,
      suffix=self.template_name_suffix)

  def get_object(self):
    slug = self.kwargs.get('slug')
    if self.model:
      return get_object_or_404(
        self.model, slug__iexact=slug)
