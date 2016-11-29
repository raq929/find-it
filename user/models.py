from django.conf import settings
from django.db import models
from item.models import House

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  slug = models.SlugField(
    max_length=30,
    unique=True)
  houses = models.ManyToManyField(House)

  def __str__(self):
    return self.user.get_username()
