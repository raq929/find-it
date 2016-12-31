from django.contrib import admin
from .models import House, Room, Place, Item

# Register your models here.
admin.site.register(House)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
  list_display = ('name', 'house')

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
  list_display = ('name', 'room', 'house')
  search_fields = ('name', 'description')
  prepopulated_fields = { "slug": ("name",)  }

  def house(self, place):
    return place.room.house

@admin.register(Item)
class PlaceAdmin(admin.ModelAdmin):
  list_display = ('name', 'place')
