from django.conf.urls import url

from ..views import (
  PlaceList, PlaceDetail, PlaceCreate, PlaceUpdate, PlaceDelete, ItemCreateFromPlace)

urlpatterns = [
  url(r'^$',
    PlaceList.as_view(),
    name='place_list'),
  url(r'^create/$',
    PlaceCreate.as_view(),
    name='place_create'),
  url(r'^update/(?P<slug>[\w\-]+)/$',
    PlaceUpdate.as_view(),
    name='place_update'),
  url(r'^delete/(?P<slug>[\w\-]+)/$',
    PlaceDelete.as_view(),
    name='place_delete'),
  url(r'^(?P<slug>[\w\-]+)/$',
    PlaceDetail.as_view(),
    name='place_detail'),
  url(r'^(?P<place_slug>[\w\-]+)/'
        r'add_item/$',
        ItemCreateFromPlace.as_view(),
        name='place_add_item'),
]
