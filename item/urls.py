from django.conf.urls import url

from .views import (
  ItemList, item_detail,
  PlaceList, place_detail,
  RoomList, room_detail,
  search)

urlpatterns = [
  url(r'^item/$',
    ItemList.as_view(),
    name='item_list'),
  url(r'^item/(?P<slug>[\w\-]+)/$',
    item_detail,
    name='item_detail'),
  url(r'^places/$',
    PlaceList.as_view(),
    name='place_list'),
  url(r'^places/(?P<slug>[\w\-]+)/$',
    place_detail,
    name='place_detail'),
  url(r'^rooms/$',
    RoomList.as_view(),
    name='room_list'),
  url(r'^rooms/(?P<slug>[\w\-]+)/$',
    room_detail,
    name='room_detail'),
  url(r'^search/$',
    search,
    name='item_search'),
]
