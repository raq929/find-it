from django.conf.urls import include, url
from django.views.generic import RedirectView

from ..views import (
  HouseCreate, HouseDelete, HouseUpdate, RoomCreate)
from . import (
  item as item_urls,
  place as place_urls,
  room as room_urls,
  house as house_urls)

urlpatterns = [
  url(r'^$', RedirectView.as_view(
    pattern_name='dj-auth:profile',
    permanent=False)),
  url(r'^create/$',
    HouseCreate.as_view(),
    name='house_create'),
  url(r'^update/(?P<slug>[\w\-]+)/$',
    HouseUpdate.as_view(),
    name='house_update'),
  url(r'^delete/(?P<slug>[\w\-]+)/$',
    HouseDelete.as_view(),
    name='house_delete'),
  url(r'^(?P<house_slug>[\w\-]+)/'
      r'room/', include(room_urls)),
  url(r'^(?P<house_slug>[\w\-]+)/'
    r'add_room/$',
    RoomCreate.as_view(),
    name='room_create'),
  url(r'^(?P<house_slug>[\w\-]+)/'
      r'place/', include(place_urls)),
  url(r'^(?P<house_slug>[\w\-]+)/'
      r'item/', include(item_urls)),
  url(r'^(?P<house_slug>[\w\-]+)/$',
      RedirectView.as_view(
        pattern_name='item_search',
        permanent=False),
      )
]
