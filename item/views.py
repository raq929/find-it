from django.http.response import HttpResponse

from .models import Room

def homepage(request):
  room_list = Room.objects.all()
  output = ', '.join(room.name for room in room_list)
  return HttpResponse(output)
