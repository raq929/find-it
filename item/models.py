from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.db import models

import itertools

class House(models.Model):
  name = models.CharField(max_length=63)
  slug = models.SlugField(
    max_length=31,
    unique=True,
    help_text='A label for URL config.')

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']

  def get_absolute_url(self):
    return reverse('house_detail',
                    kwargs={ 'slug': self.slug })

  def get_update_url(self):
    return reverse('house_update',
                    kwargs={ 'slug': self.slug })

  def get_delete_url(self):
    return reverse('house_delete',
                    kwargs={ 'slug': self.slug })

  def get_search_url(self):
    return reverse('item_search',
                    kwargs={ 'house_slug': self.slug })

  def get_room_list_url(self):
    return reverse('room_list',
      kwargs={'house_slug': self.slug})

  def get_place_list_url(self):
    return reverse('place_list',
      kwargs={'house_slug': self.slug})

  def get_item_list_url(self):
    return reverse('item_list',
      kwargs={'house_slug': self.slug})

  def get_room_create_url(self):
    return reverse('room_create',
      kwargs={ 'house_slug': self.slug })

  def get_place_create_url(self):
    return reverse('place_create',
      kwargs={ 'house_slug': self.slug })

  def get_item_create_url(self):
    return reverse('item_create',
      kwargs={ 'house_slug': self.slug })

  def get_search_url(self):
    return reverse('item_search',
                   kwargs={ 'house_slug': self.slug })


class Room(models.Model):
  name = models.CharField(max_length=63)
  slug = models.SlugField(
    max_length=31,
    unique=True,
    help_text='A label for URL config.')
  house = models.ForeignKey(House, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']
    unique_together = ('slug', 'house')

  def get_absolute_url(self):
    return reverse('room_detail',
                    kwargs={ 'room_slug': self.slug,
                             'house_slug': self.house.slug })
  def get_list_url(self):
    return reverse('room_list',
                    kwargs={ 'house_slug': self.house.slug })

  def get_create_url(self):
    return reverse('room_create',
                    kwargs={ 'house_slug': self.house.slug })

  def get_update_url(self):
    return reverse('room_update',
                    kwargs={ 'room_slug': self.slug,
                            'house_slug': self.house.slug })

  def get_delete_url(self):
    return reverse('room_delete',
                    kwargs={ 'room_slug': self.slug,
                            'house_slug': self.house.slug })




class Place(models.Model):
  name = models.CharField(max_length=63)
  slug = models.SlugField(max_length=31,
    help_text='A label for URL config.')
  description = models.TextField()
  room = models.ForeignKey(Room, on_delete=models.CASCADE)

  def __str__(self):
    return "{} in {}".format(self.name, self.room)

  def clean(self):
    if self.slug and self.room:
      # find the house
      house = self.room.house
      # find all place slugs in the house
      rooms = house.room_set.all() # querySet
      places = [room.place_set.all() for room in rooms] # list of querySets
      place_slugs = [place.slug for place in itertools.chain(*places) if place.id != self.id] # list of slug strings
      # check that slug is different from all other place slugs
      if self.slug in place_slugs:
        raise(ValidationError('Place slug must be unique within it\'s house'))

    return super().clean()

  class Meta:
    ordering = ['name']

  def get_absolute_url(self):
    return reverse('place_detail',
                    kwargs={ 'place_slug': self.slug,
                              'house_slug': self.room.house.slug,
                    })

  def get_list_url(self):
    return reverse('place_list',
                    kwargs={ 'house_slug': self.room.house.slug })

  def get_create_url(self):
    return reverse('place_create',
                    kwargs={ 'house_slug': self.room.house.slug })

  def get_update_url(self):
    return reverse('place_update',
                    kwargs={ 'place_slug': self.slug,
                            'house_slug': self.room.house.slug })

  def get_delete_url(self):
    return reverse('place_delete',
                    kwargs={ 'place_slug': self.slug,
                            'house_slug': self.room.house.slug })

  def get_item_create_url(self):
    return reverse('place_add_item',
                    kwargs={ 'place_slug': self.slug,
                             'house_slug': self.room.house.slug })


class Item(models.Model):
  name = models.CharField(
    max_length=63,
    unique=True)
  slug = models.SlugField(
    max_length=31,
    help_text='A label for URL config.')
  date_updated = models.DateField('date last seen in this place')
  place = models.ForeignKey(Place, on_delete=models.CASCADE)

  def __str__(self):
    return "{} in {}".format(self.name, self.place)

  def clean(self):
    if self.slug and self.place:
      # find the house
      house = self.place.room.house
      # find all place slugs in the house
      rooms = house.room_set.all() # querySet
      places = [room.place_set.all() for room in rooms] # list of querySets
      items = [place.item_set.all() for place in itertools.chain(*places)] # list of item querySets
      item_slugs = [item.slug for item in itertools.chain(*items) if item.id != self.id]
      # check that slug is different from all other place slugs
      if self.slug in item_slugs:
        raise(ValidationError('Item slug must be unique within it\'s house'))

    return super().clean()

  class Meta:
    ordering = ['name']

  def get_absolute_url(self):
    return reverse('item_detail',
                    kwargs={ 'item_slug': self.slug,
                             'house_slug': self.place.room.house.slug })

  def get_list_url(self):
    return reverse('item_list',
                    kwargs={ 'house_slug': self.place.room.house.slug })

  def get_create_url(self):
    return reverse('item_create',
                    kwargs={ 'house_slug': self.place.room.house.slug })

  def get_update_url(self):
    return reverse('item_update',
                    kwargs={ 'item_slug': self.slug,
                             'house_slug': self.place.room.house.slug })

  def get_delete_url(self):
    return reverse('item_delete',
                    kwargs={ 'item_slug': self.slug,
                             'house_slug': self.place.room.house.slug })

