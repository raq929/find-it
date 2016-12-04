from django.conf.urls import include, url
from django.views.generic import RedirectView

from ..views import (
  HouseCreate)
from . import (
  item as item_urls,
  place as place_urls,
  room as room_urls,
  house as house_urls)

urlpatterns = [
  url(r'^create/$',
    HouseCreate.as_view(),
    name='house_create'),
  url(r'^(?P<house_slug>[\w\-]+)/'
      r'room/', include(room_urls)),
]
