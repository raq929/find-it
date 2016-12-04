from django.conf.urls import url

from ..views import (
  HouseCreate)

urlpatterns = [
  url(r'^create/$',
    HouseCreate.as_view(),
    name='house_create'),
]
