from django import forms
from django.core.exceptions import ValidationError

from .models import Room, Place, Item, House
from user.models import Profile

class SlugCleanMixin:
  """Mixin class for slug cleaning method."""

  def clean_slug(self):
    new_slug = (
      self.cleaned_data['slug'].lower())
    if new_slug == 'create' or new_slug == 'update':
      raise ValidationError(
        'Slug may not be "create" or "update"')
    return new_slug

class RoomForm(SlugCleanMixin, forms.ModelForm):
  class Meta:
    model = Room
    fields = '__all__'

class PlaceForm(SlugCleanMixin, forms.ModelForm):
  class Meta:
    model = Place
    fields = '__all__'

class ItemForm(SlugCleanMixin, forms.ModelForm):
  class Meta:
    model = Item
    fields = '__all__'

class HouseForm(SlugCleanMixin, forms.ModelForm):
  def __init__(self, *args, **kwargs):
    if 'user' in kwargs:
      self.user = kwargs.pop('user')
    # print(**kwargs)
    super(HouseForm, self).__init__(*args, **kwargs)

  def save(self, **kwargs):
    house = super().save()
    profile = self.user.profile
    profile.houses.add(house)
    return house

  class Meta:
    model = House
    fields = '__all__'
