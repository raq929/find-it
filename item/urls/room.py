from django.conf.urls import url

from ..views import (
  RoomList, RoomDetail, RoomUpdate, RoomDelete,
  search)

urlpatterns = [
   url(r'^$',
    RoomList.as_view(),
    name='room_list'),
  url(r'^update/(?P<room_slug>[\w\-]+)/$',
    RoomUpdate.as_view(),
    name='room_update'),
  url(r'^delete/(?P<room_slug>[\w\-]+)/$',
    RoomDelete.as_view(),
    name='room_delete'),
  url(r'^(?P<room_slug>[\w\-]+)/$',
    RoomDetail.as_view(),
    name='room_detail'),
]
