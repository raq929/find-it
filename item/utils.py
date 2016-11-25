from django.shortcuts import get_object_or_404, render
from django.views.generic import View

class DetailView(View):
  context_object_name = ''
  model = None
  template_name = ''

  def get(self, request, slug):
    obj = get_object_or_404(self.model, slug__iexact=slug)
    return render(
      request,
      self.template_name,
      { self.context_object_name: obj })
