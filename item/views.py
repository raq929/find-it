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
from .models import Item, Place, Room
from .forms import RoomForm, PlaceForm, ItemForm, HouseForm
from .utils import PageLinksMixin, PlaceContextMixin

@require_authenticated_permission('item.add_item')
class ItemCreate(CreateView):
  form_class = ItemForm
  template_name = 'item/item_form.html'

@require_authenticated_permission('item.add_item')
class ItemCreateFromPlace(PlaceContextMixin, ItemCreate):
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
class ItemDelete(DeleteView):
  model = Item
  success_url = reverse_lazy('item_list')

@require_authenticated_permission('item.change_item')
class ItemUpdate(UpdateView):
  form_class = ItemForm
  model = Item
  template_name = (
    'item/item_update_form.html')

class ItemList(PageLinksMixin, ListView):
  model = Item
  page_kwarg = 'page'
  paginate_by = 5 # 5 items per page


class ItemDetail(DetailView):
  model = Item

@require_authenticated_permission('item.add_place')
class PlaceCreate(CreateView):
  form_class = PlaceForm
  template_name = 'item/place_form.html'

class PlaceList(PageLinksMixin, ListView):
  model = Place
  page_kwarg = 'page'
  paginate_by = 5


class PlaceDetail(DetailView):
  model = Place

@require_authenticated_permission('item.delete_place')
class PlaceDelete(DeleteView):
  model = Place
  success_url = reverse_lazy('place_list')

@require_authenticated_permission('item.change_place')
class PlaceUpdate(UpdateView):
  form_class= PlaceForm
  model = Place
  template_name = (
    'item/place_update_form.html')

@require_authenticated_permission('item.add_room')
class RoomCreate(CreateView):
  form_class = RoomForm
  template_name = 'item/room_form.html'

class RoomList(ListView):
  model = Room

class RoomDetail(DetailView):
  model = Room

@require_authenticated_permission('item.delete_room')
class RoomDelete(DeleteView):
  model = Room
  success_url = reverse_lazy('room_list')

@require_authenticated_permission('item.change_room')
class RoomUpdate(UpdateView):
  form_class= RoomForm
  model = Room
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
