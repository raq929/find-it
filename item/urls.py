from django.conf.urls import url

from .views import (
  ItemList, item_detail)

urlpatterns = [
  url(r'^$',
    ItemList.as_view(),
    name='item_list'),
  url(r'^(?P<slug>[\w\-]+)/$',
    item_detail,
    name='item_detail'),
]
