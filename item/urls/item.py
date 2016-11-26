from django.conf.urls import url

from ..views import (
  ItemList, ItemDetail, ItemCreate,  ItemUpdate, ItemDelete,
  search)

urlpatterns = [
  url(r'^$',
    ItemList.as_view(),
    name='item_list'),
  url(r'^create/$',
    ItemCreate.as_view(),
    name='item_create'),
  url(r'^update/(?P<slug>[\w\-]+)/$',
    ItemUpdate.as_view(),
    name='item_update'),
  url(r'^delete/(?P<slug>[\w\-]+)/$',
    ItemDelete.as_view(),
    name='item_delete'),
  url(r'^search/$',
    search,
    name='item_search'),
  url(r'^(?P<slug>[\w\-]+)/$',
    ItemDetail.as_view(),
    name='item_detail'),
]
