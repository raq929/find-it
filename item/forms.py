from django import forms

from .models import Room, Place, Item

class SlugCleanMixin:
  """Mixin class for slug cleaning method."""

  def clean_slug(self):
    new_slug = (
      self.cleaned_data['slug'].lower())
    if new_slug == 'create':
      raise ValidationError(
        'Slug may not be "create".')
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
