from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView,
  DetailView, ListView, UpdateView, View)
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator)
from django.core.urlresolvers import reverse_lazy

from user.decorators import (
  class_login_required,
  require_authenticated_permission)
from .search import get_query, normalize_query
from .models import Item, Place, Room, House
from .forms import RoomForm, PlaceForm, ItemForm, HouseForm
from .utils import (HouseContextMixin,
  PageLinksMixin, PlaceContextMixin,
  AddHouseToFormMixin, GetObjectByHouseMixin,
  GetListByHouseMixin, HouseFormFieldsMixin)

@require_authenticated_permission('item.add_item')
class ItemCreate(CreateView):
  form_class = ItemForm
  template_name = 'item/item_form.html'

@require_authenticated_permission('item.add_item')
class ItemCreateFromPlace(PlaceContextMixin, HouseContextMixin, ItemCreate):
  def get_initial(self):
    if self.request.method == 'GET':
      place_slug = self.kwargs.get(
        self.place_slug_url_kwarg)
      self.place = get_object_or_404(
        Place,
        slug__iexact=place_slug)
      initial = {
        self.place_context_object_name:
          self.place,
      }
      initial.update(self.initial)
      return initial
    return super().get_initial()

@require_authenticated_permission('item.delete_item')
class ItemDelete(HouseContextMixin, GetObjectByHouseMixin, DeleteView):
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  slug_url_kwarg = 'item_slug'
  def get_success_url(self):
        return (self.object.get_list_url())

@require_authenticated_permission('item.change_item')
class ItemUpdate(HouseContextMixin, GetObjectByHouseMixin, UpdateView):
  form_class = ItemForm
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  slug_url_kwarg = 'item_slug'
  template_name = (
    'item/item_update_form.html')

class ItemList(HouseContextMixin, GetListByHouseMixin, PageLinksMixin, ListView):
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  page_kwarg = 'page'
  paginate_by = 5 # 5 items per page


class ItemDetail(HouseContextMixin, GetObjectByHouseMixin, DetailView):
  model = Item
  slug_url_kwarg = 'item_slug'
  house_slug_keyword = 'place__room__house__slug__iexact'

@require_authenticated_permission('item.add_place')
class PlaceCreate(HouseContextMixin, HouseFormFieldsMixin, CreateView):
  form_class = PlaceForm
  template_name = 'item/place_form.html'

class PlaceList(HouseContextMixin, GetListByHouseMixin, PageLinksMixin, ListView):
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  page_kwarg = 'page'
  paginate_by = 5


class PlaceDetail(HouseContextMixin, GetObjectByHouseMixin, DetailView):
  model = Place
  slug_url_kwarg = 'place_slug'
  house_slug_keyword = 'room__house__slug__iexact'

@require_authenticated_permission('item.delete_place')
class PlaceDelete(HouseContextMixin, GetObjectByHouseMixin, DeleteView):
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  slug_url_kwarg = 'place_slug'
  def get_success_url(self):
        return (self.object.get_list_url())

@require_authenticated_permission('item.change_place')
class PlaceUpdate(HouseContextMixin, GetObjectByHouseMixin, UpdateView):
  form_class= PlaceForm
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  slug_url_kwarg = 'place_slug'
  template_name = (
    'item/place_update_form.html')

@require_authenticated_permission('item.add_room')
class RoomCreate(HouseContextMixin,
  AddHouseToFormMixin, GetObjectByHouseMixin, CreateView):
  form_class = RoomForm
  template_name = 'item/room_form.html'

  def get_initial(self):
    house_slug = self.kwargs.get(self.house_slug_url_kwarg)
    self.house = get_object_or_404(House, slug__iexact=house_slug)
    initial = {
      self.house_context_object_name:
        self.house
    }
    initial.update(self.initial)
    return initial


class RoomList(HouseContextMixin, GetListByHouseMixin, ListView):
  model = Room
  slug_url_kwarg = 'room_slug'
  house_slug_keyword = 'house__slug__iexact'

class RoomDetail(HouseContextMixin,
  GetObjectByHouseMixin, DetailView):
  model = Room
  slug_url_kwarg = 'room_slug'
  house_slug_keyword = 'house__slug__iexact'

@require_authenticated_permission('item.delete_room')
class RoomDelete(HouseContextMixin,
  GetObjectByHouseMixin, DeleteView):
  model = Room
  slug_url_kwarg = 'room_slug'
  house_slug_keyword = 'house__slug__iexact'

  def get_success_url(self):
        return (self.object.get_list_url())

@require_authenticated_permission('item.change_room')
class RoomUpdate(HouseContextMixin,
  GetObjectByHouseMixin, UpdateView):
  form_class= RoomForm
  model = Room
  slug_url_kwarg = 'room_slug'
  house_slug_keyword = 'house__slug__iexact'
  template_name = (
    'item/room_update_form.html')


class HouseCreate(CreateView):
  form_class = HouseForm
  template_name = 'item/house_form.html'
  success_url = reverse_lazy('dj-auth:profile')

  def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                'user': self.request.user
            })
        return kwargs


# search

def search(request):
    query_string = ''
    found_items = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['name'])

        found_items = Item.objects.filter(entry_query)

    return render(request,
                  'item/item_search.html',
                  { 'query_string': query_string, 'found_items': found_items },
                )
