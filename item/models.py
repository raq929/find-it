from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models

class Room(models.Model):
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
    return reverse('room_detail',
      kwargs={ 'slug': self.slug })

class Place(models.Model):
  name = models.CharField(max_length=63)
  slug = models.SlugField(max_length=31,
    unique=True,
    help_text='A label for URL config.')
  description = models.TextField()
  room = models.ForeignKey(Room)

  def __str__(self):
    return "{} in {}".format(self.name, self.room)

  class Meta:
    ordering = ['name']

  def get_absolute_url(self):
    return reverse('place_detail',
      kwargs={ 'slug': self.slug })


class Item(models.Model):
  name = models.CharField(
    max_length=63,
    unique=True)
  slug = models.SlugField(
    max_length=31,
    unique=True,
    help_text='A label for URL config.')
  date_updated = models.DateField('date last seen in this place')
  place = models.ForeignKey(Place)

  def __str__(self):
    return "{} in {}".format(self.name, self.place)

  class Meta:
    ordering = ['name']

  def get_absolute_url(self):
    return reverse('item_detail',
      kwargs={ 'slug': self.slug })

