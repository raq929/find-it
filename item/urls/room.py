from django.conf.urls import url

from ..views import (
  ItemList, ItemDetail, ItemCreate, ItemCreateFromPlace, ItemUpdate, ItemDelete,
  PlaceList, PlaceDetail, PlaceCreate, PlaceUpdate, PlaceDelete,
  RoomList, RoomDetail, RoomCreate, RoomUpdate, RoomDelete,
  search)

urlpatterns = [
   url(r'^$',
    RoomList.as_view(),
    name='room_list'),
  url(r'^create/$',
    RoomCreate.as_view(),
    name='room_create'),
  url(r'^update/(?P<slug>[\w\-]+)/$',
    RoomUpdate.as_view(),
    name='room_update'),
  url(r'^delete/(?P<slug>[\w\-]+)/$',
    RoomDelete.as_view(),
    name='room_delete'),
  url(r'^(?P<slug>[\w\-]+)/$',
    RoomDetail.as_view(),
    name='room_detail'),
]
