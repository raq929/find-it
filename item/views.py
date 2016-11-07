from django.shortcuts import get_object_or_404, render
from django.views.generic import View
import re
from django.db.models import Q

from .models import Item, Place, Room

class ItemList(View):
  def get(self, request):
    return render(
      request,
      'item/item_list.html',
      {'item_list': Item.objects.all() })

def item_detail(request, slug):
  item = get_object_or_404(Item, slug__iexact=slug)
  return render(request,
    'item/item_detail.html',
    { 'item': item })

class PlaceList(View):
  def get(self, request):
    return render(
      request,
      'item/place_list.html',
      {'place_list': Place.objects.all() })

def place_detail(request, slug):
  place = get_object_or_404(Place, slug__iexact=slug)
  return render(request,
    'item/place_detail.html',
    { 'place': place })

class RoomList(View):
  def get(self, request):
    return render(
      request,
      'item/room_list.html',
      {'room_list': Room.objects.all() })

def room_detail(request, slug):
  room = get_object_or_404(Room, slug__iexact=slug)
  return render(request,
    'item/room_detail.html',
    { 'room': room })


# search

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


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


