from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView,
  DetailView, ListView, UpdateView, View)
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator)
from django.core.urlresolvers import reverse_lazy

from .search import get_query, normalize_query
from .models import Item, Place, Room
from .forms import RoomForm, PlaceForm, ItemForm
from .utils import PageLinksMixin

class ItemCreate(CreateView):
  form_class = ItemForm
  template_name = 'item/item_form.html'

class ItemDelete(DeleteView):
  model = Item
  success_url = reverse_lazy('item_list')

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


class PlaceCreate(CreateView):
  form_class = PlaceForm
  template_name = 'item/place_form.html'

class PlaceList(PageLinksMixin, ListView):
  model = Place
  page_kwarg = 'page'
  paginate_by = 5


class PlaceDetail(DetailView):
  model = Place

class PlaceDelete(DeleteView):
  model = Place
  success_url = reverse_lazy('place_list')

class PlaceUpdate(UpdateView):
  form_class= PlaceForm
  model = Place
  template_name = (
    'item/place_update_form.html')

class RoomCreate(CreateView):
  form_class = RoomForm
  template_name = 'item/room_form.html'

class RoomList(ListView):
  model = Room

class RoomDetail(DetailView):
  model = Room


class RoomDelete(DeleteView):
  model = Room
  success_url = reverse_lazy('room_list')


class RoomUpdate(UpdateView):
  form_class= RoomForm
  model = Room
  template_name = (
    'item/room_update_form.html')

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
