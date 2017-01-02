from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView,
  DetailView, ListView, UpdateView, View)
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator)
from django.core.urlresolvers import reverse_lazy

from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm

from user.decorators import (
  class_login_required,
  require_authenticated_permission)
from .search import get_query, normalize_query
from .models import Item, Place, Room, House
from .forms import RoomForm, PlaceForm, ItemForm, HouseForm
from .utils import (HouseContextMixin,
  PageLinksMixin, HousePlaceContextMixin,
  AddHouseToFormMixin, GetObjectByHouseMixin,
  GetListByHouseMixin, HouseFormFieldsMixin)


class BaseItemCreate(HouseFormFieldsMixin,
                 PermissionRequiredMixin, CreateView):
  form_class = ItemForm
  permission_required = ['change_house']
  template_name = 'item/item_form.html'

class ItemCreate(HouseContextMixin, BaseItemCreate):
  pass

class ItemCreateFromPlace(HousePlaceContextMixin, BaseItemCreate):
  def get_initial(self):
    if self.request.method == 'GET':

      if not hasattr(self, 'place'):
        place_slug = self.kwargs.get(
          self.place_slug_url_kwarg)
      else:
        place_slug = self.place.slug

      if not hasattr(self, 'house'):
        house_slug = self.kwargs.get(
          self.house_slug_url_kwarg)
      else:
        house_slug = self.house.slug

      self.place = get_object_or_404(
          Place,
          slug__iexact=place_slug,
          room__house__slug__iexact=house_slug)
      initial = {
        self.place_context_object_name:
          self.place,
      }
      initial.update(self.initial)
      return initial
    return super().get_initial()

class ItemDelete(HouseContextMixin, GetObjectByHouseMixin,
                 PermissionRequiredMixin, DeleteView):
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  slug_url_kwarg = 'item_slug'
  permission_required = ['change_house']
  queryset = Item.objects.select_related('place__room__house')

  def get_success_url(self):
        return (self.object.get_list_url())

class ItemUpdate(HouseContextMixin, GetObjectByHouseMixin,
                 HouseFormFieldsMixin, PermissionRequiredMixin, UpdateView):
  form_class = ItemForm
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  permission_required = ['change_house']
  slug_url_kwarg = 'item_slug'
  template_name = (
    'item/item_update_form.html')
  queryset = Item.objects.select_related('place__room__house')

class ItemList(HouseContextMixin, GetListByHouseMixin, PageLinksMixin,
               PermissionRequiredMixin, ListView):
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  page_kwarg = 'page'
  paginate_by = 5 # 5 items per page
  permission_required = ['view_house']
  queryset = Item.objects.select_related('place__room__house')


class ItemDetail(HouseContextMixin, GetObjectByHouseMixin, PermissionRequiredMixin,
                 DetailView):
  house_slug_keyword = 'place__room__house__slug__iexact'
  model = Item
  permission_required = ['view_house']
  queryset = Item.objects.select_related('place__room__house')
  slug_url_kwarg = 'item_slug'


class PlaceCreate(HouseContextMixin, HouseFormFieldsMixin, PermissionRequiredMixin,
                  CreateView):
  form_class = PlaceForm
  permission_required = ['change_house']
  template_name = 'item/place_form.html'


class PlaceList(HouseContextMixin, GetListByHouseMixin, PageLinksMixin,
  PermissionRequiredMixin, ListView):
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  page_kwarg = 'page'
  paginate_by = 5
  permission_required = ['view_house']
  queryset = Place.objects.select_related('room__house')


class PlaceDetail(HouseContextMixin, GetObjectByHouseMixin,
                  PermissionRequiredMixin, DetailView):
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  permission_required = ['view_house']
  queryset = Place.objects.select_related('room__house')
  slug_url_kwarg = 'place_slug'


class PlaceDelete(HouseContextMixin, GetObjectByHouseMixin, PermissionRequiredMixin,
                  DeleteView):
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  permission_required = ['change_house']
  queryset = Place.objects.select_related('room__house')
  slug_url_kwarg = 'place_slug'

  def get_success_url(self):
        return (self.object.get_list_url())


class PlaceUpdate(HouseContextMixin, GetObjectByHouseMixin,
                  HouseFormFieldsMixin, PermissionRequiredMixin, UpdateView):
  form_class= PlaceForm
  house_slug_keyword = 'room__house__slug__iexact'
  model = Place
  permission_required = ['change_house']
  slug_url_kwarg = 'place_slug'
  template_name = (
    'item/place_update_form.html')
  queryset = Place.objects.select_related('room__house')


class RoomCreate(HouseContextMixin,
  AddHouseToFormMixin, PermissionRequiredMixin, CreateView):
  form_class = RoomForm
  house_slug_keyword = 'house__slug__iexact'
  permission_required = ['change_house']
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

class RoomList(HouseContextMixin, GetListByHouseMixin,
  PermissionRequiredMixin, ListView):
  house_slug_keyword = 'house__slug__iexact'
  model = Room
  permission_required = ['view_house',]
  queryset = Room.objects.select_related('house')
  slug_url_kwarg = 'room_slug'

class RoomDetail(HouseContextMixin,
  GetObjectByHouseMixin, PermissionRequiredMixin, DetailView):
  house_slug_keyword = 'house__slug__iexact'
  model = Room
  permission_required = ['view_house',]
  queryset = Room.objects.select_related('house')
  slug_url_kwarg = 'room_slug'

class RoomDelete(HouseContextMixin,
  GetObjectByHouseMixin, PermissionRequiredMixin, DeleteView):
  house_slug_keyword = 'house__slug__iexact'
  model = Room
  permission_required = ['delete_house',]
  queryset = Room.objects.select_related('house')
  slug_url_kwarg = 'room_slug'

  def get_success_url(self):
        return (self.object.get_list_url())

class RoomUpdate(HouseContextMixin,
  GetObjectByHouseMixin, PermissionRequiredMixin, UpdateView):
  form_class= RoomForm
  house_slug_keyword = 'house__slug__iexact'
  model = Room
  permission_required = ['change_house',]
  slug_url_kwarg = 'room_slug'
  template_name = (
    'item/room_update_form.html')
  queryset = Room.objects.select_related('house')


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

  def form_valid(self, *args, **kwargs):
        resp = super(HouseCreate, self).form_valid(*args, **kwargs)
        assign_perm('view_house', self.request.user, self.object)
        assign_perm('change_house', self.request.user, self.object)
        assign_perm('delete_house', self.request.user, self.object)
        return resp


class HouseDelete(DeleteView, PermissionRequiredMixin):
  model = House
  permission_required = ['delete_house']

  def get_success_url(self):
        return reverse_lazy('dj-auth:profile')

class HouseUpdate(UpdateView, PermissionRequiredMixin):
  form_class= HouseForm
  model = House
  permission_required = ['change_house']
  template_name = (
    'item/house_update_form.html')

# search
def search(request, house_slug=None):
    query_string = ''
    found_items = None

    if(house_slug):
      house = house = get_object_or_404(
      House,
      slug__iexact=house_slug)

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['name'])

        found_items = Item.objects.filter(entry_query, place__room__house__slug=house_slug)

    return render(request,
                  'item/item_search.html',
                  { 'query_string': query_string, 'found_items': found_items, 'house': house },
                )
