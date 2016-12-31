from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


from .models import Place, House, Room

class HouseContextMixin():
  """Adds the current house to the context for rendering"""
  house_slug_url_kwarg = 'house_slug'
  house_context_object_name = 'house'

  def get_context_data(self, **kwargs):
    if hasattr(self, 'house'):
      context = {
        self.place_context_object_name:
            self.house,
      }
    house_slug = self.kwargs.get(
      self.house_slug_url_kwarg)
    house = get_object_or_404(
      House,
      slug__iexact=house_slug)
    context = {
      self.house_context_object_name:
        house,
    }
    context.update(kwargs)
    return super().get_context_data(**context)

class HouseFormFieldsMixin():
  """ensures that form choices are limited to the house"""
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    house_slug = self.kwargs.get(
      self.house_slug_url_kwarg)
    house = {
      'house_slug':
        house_slug,
    }
    new_kwargs = kwargs.update(house)
    return kwargs


class GetObjectByHouseMixin():
  """Gets an object within a specified house"""
  def get_object(self, queryset=None):
    house_slug = self.kwargs.get(
      self.house_slug_url_kwarg)
    slug = self.kwargs.get(self.slug_url_kwarg)
    house_slug_keyword = self.house_slug_keyword
    slug_args = {
      'slug__iexact': slug,
      house_slug_keyword: house_slug,
    }
    return get_object_or_404(
      self.model,
      **slug_args)

class GetListByHouseMixin():
  """Gets a list of objects within a specified house"""
  def get_queryset(self):
    house_slug = self.kwargs.get(
        self.house_slug_url_kwarg)
    house_slug_keyword = self.house_slug_keyword
    model = self.model
    house_filter = {
      house_slug_keyword: house_slug
    }
    return model.objects.all().filter(**house_filter)


class PlaceContextMixin():
  """Adds the current place to the context"""
  place_slug_url_kwarg = 'place_slug'
  place_context_object_name = 'place'

  def get_context_data(self, **kwargs):
    if hasattr(self, 'place'):
      context = {
        self.place_context_object_name:
            self.place,
      }
    else:
      place_slug = self.kwargs.get(
        self.place_slug_url_kwarg)
      place = get_object_or_404(
        Place,
        slug__iexact=place_slug)
      context = {
        self.place_context_object_name:
          place,
      }
    context.update(kwargs)
    return super().get_context_data(**context)

class PageLinksMixin:
  """Mixin class for adding links the context object
   for previous and next pages"""
  page_kwarg = 'page'

  def first_page(self, page):
    # don't show on first page
    if page.number > 1:
      return self._page_urls(1)
    return None

  def last_page(self, page):
      last_page = page.paginator.num_pages
      if page.number < last_page:
        return self._page_urls(last_page)
      return None

  def _page_urls(self, page_number):
    return "?{pkw}={n}".format(
      pkw=self.page_kwarg,
      n=page_number)

  def previous_page(self, page):
    if (page.has_previous()
            and page.number > 2):
      return self._page_urls(
        page.previous_page_number())
    return None

  def next_page(self, page):
    last_page = page.paginator.num_pages
    if (page.has_next()
          and page.number < last_page - 1):
      return self._page_urls(
        page.next_page_number())
    return None

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    page = context.get('page_obj')
    if page is not None:
      context.update({
          'first_page_url':
            self.first_page(page),
          'last_page_url':
            self.last_page(page),
          'previous_page_url':
            self.previous_page(page),
          'next_page_url':
            self.next_page(page),
        })
    return context

class AddHouseToFormMixin():
  """Adds the current house to the form and saves it"""
  def form_valid(self, form):
    house = get_object_or_404(
      House,
      slug__iexact=self.kwargs.get(self.house_slug_url_kwarg))
    self.object = form.save(
      house_obj=house)
    return HttpResponseRedirect(self.get_success_url())

