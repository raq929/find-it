from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, View
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator)

from .search import get_query, normalize_query
from .models import Item, Place, Room
from .forms import RoomForm, PlaceForm, ItemForm
from .utils import DetailView




class ItemCreate(CreateView):
  form_class = ItemForm
  template_name = 'item/item_form.html'

class ItemDelete(View):

  def get(self, request, slug):
    item = get_object_or_404(
      Item, slug__iexact=slug)
    return render(
      request,
      'item/item_confirm_delete.html'
      , { 'item': item })

  def post(self, request, slug):
    item = get_object_or_404(
      Item, slug__iexact=slug)
    place = item.place
    item.delete()
    return redirect(place)


class ItemUpdate(View):
  form_class= ItemForm
  template_name = (
    'item/item_update_form.html')

  def get(self, request, slug):
    item = get_object_or_404(
      Item, slug__iexact=slug)
    context = {
      'form': self.form_class(instance=item),
      'item': item,
    }
    return render(
      request, self.template_name, context)

  def post(self, request, slug):
    item = get_object_or_404(
      Item, slug__iexact=slug)
    bound_form = self.form_class(
      request.POST, instance=item)
    if bound_form.is_valid():
      new_item = bound_form.save()
      return redirect(new_item)
    else:
      context = {
        'form': bound_form,
        'item': item,
      }
      return render(
        request, self.template_name, context)

class ItemList(View):
  page_kwarg = 'page'
  paginate_by = 5 # 5 items per page
  template_name = 'item/item_list.html'

  def get(self, request):
    items = Item.objects.all()
    page_number = request.GET.get(self.page_kwarg)
    paginator = Paginator(
      items, self.paginate_by)

    try:
      page = paginator.page(page_number)
    except PageNotAnInteger:
      page = paginator.page(1)
    except EmptyPage:
      page = paginator.page(paginator.num_pages)

    if page.has_previous():
      prev_url = "?{pkw}={n}".format(
        pkw=self.page_kwarg,
        n=page.previous_page_number())
    else:
      prev_url = None

    if page.has_next():
      next_url = "?{pkw}={n}".format(
        pkw=self.page_kwarg,
        n=page.next_page_number())
    else:
      next_url = None

    context = {
      'is_paginated': page.has_other_pages(),
      'next_page_url': next_url,
      'paginator': paginator,
      'previous_page_url': prev_url,
      'item_list': page,
    }

    return render(
      request,
      self.template_name,
      context)

class ItemDetail(DetailView):
  model = Item


class PlaceCreate(CreateView):
  form_class = PlaceForm
  template_name = 'item/place_form.html'

class PlaceList(View):
  def get(self, request):
    return render(
      request,
      'item/place_list.html',
      {'place_list': Place.objects.all() })

class PlaceDetail(DetailView):
  model = Place

class PlaceDelete(View):

  def get(self, request, slug):
    place = get_object_or_404(
      Place, slug__iexact=slug)
    return render(
      request,
      'item/place_confirm_delete.html'
      , { 'place': place })

  def post(self, request, slug):
    place = get_object_or_404(
      Place, slug__iexact=slug)
    room = place.room
    place.delete()
    return redirect(room)


class PlaceUpdate(View):
  form_class= PlaceForm
  template_name = (
    'item/place_update_form.html')

  def get(self, request, slug):
    place = get_object_or_404(
      Place, slug__iexact=slug)
    context = {
      'form': self.form_class(instance=place),
      'place': place,
    }
    return render(
      request, self.template_name, context)

  def post(self, request, slug):
    place = get_object_or_404(
      Place, slug__iexact=slug)
    bound_form = self.form_class(
      request.POST, instance=place)
    if bound_form.is_valid():
      new_place = bound_form.save()
      return redirect(new_place)
    else:
      context = {
        'form': bound_form,
        'place': place,
      }
      return render(
        request, self.template_name, context)

class RoomCreate(CreateView):
  form_class = RoomForm
  template_name = 'item/room_form.html'

class RoomList(View):
  def get(self, request):
    return render(
      request,
      'item/room_list.html',
      {'room_list': Room.objects.all() })

class RoomDetail(DetailView):
  model = Room


class RoomDelete(View):

  def get(self, request, slug):
    room = get_object_or_404(
      Room, slug__iexact=slug)
    return render(
      request,
      'item/room_confirm_delete.html'
      , { 'room': room })

  def post(self, request, slug):
    room = get_object_or_404(
      Room, slug__iexact=slug)
    room.delete()
    return redirect('item_search')


class RoomUpdate(View):
  form_class= RoomForm
  template_name = (
    'item/room_update_form.html')

  def get(self, request, slug):
    room = get_object_or_404(
      Room, slug__iexact=slug)
    context = {
      'form': self.form_class(instance=room),
      'room': room,
    }
    return render(
      request, self.template_name, context)

  def post(self, request, slug):
    place = get_object_or_404(
      Room, slug__iexact=slug)
    bound_form = self.form_class(
      request.POST, instance=place)
    if bound_form.is_valid():
      new_place = bound_form.save()
      return redirect(new_place)
    else:
      context = {
        'form': bound_form,
        'place': place,
      }
      return render(
        request, self.template_name, context)



# search

def search(request):
    query_string = ''
    found_items = None
    print 'got here'
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        print query_string

        entry_query = get_query(query_string, ['name'])

        found_items = Item.objects.filter(entry_query)

    return render(request,
                  'item/item_search.html',
                  { 'query_string': query_string, 'found_items': found_items },
                )


