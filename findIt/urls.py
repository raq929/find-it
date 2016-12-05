"""findIt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from item.urls import (
  item as item_urls,
  place as place_urls,
  room as room_urls,
  house as house_urls)
from user import urls as user_urls

urlpatterns = [
  url(r'^$', RedirectView.as_view(
      pattern_name='dj-auth:login',
      permanent=False)),
  url(r'^admin/', admin.site.urls),
  url(r'^about/$', TemplateView.as_view(
    template_name='site/about.html'),
    name='about_site'),
  url(r'^item/', include(item_urls)),
  url(r'^place/', include(place_urls)),
  url(r'^user/', include(
    user_urls,
    app_name='user',
    namespace='dj-auth')),
  url(r'^', include(house_urls)),
]
