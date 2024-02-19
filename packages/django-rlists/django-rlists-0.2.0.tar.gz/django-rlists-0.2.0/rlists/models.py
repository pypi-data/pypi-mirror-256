import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Rlist(models.Model):

    rlist_file = models.FileField(upload_to='ratinglists/')

    rlist_filename = models.CharField(max_length=100, blank=True, null=True)

    slug = str(uuid.uuid4)

    def __str__(self):
        return self.slug


class Player(models.Model):

    origin_file =  models.CharField(max_length=20, blank=True, null=True)

    name = models.CharField(max_length=100, blank=True, null=True)

    rating = models.CharField(max_length=100, blank=True, null=True)

    fed = models.CharField(max_length=20, blank=True, null=True)

    birthday = models.CharField(max_length=100, blank=True, null=True)

    slug = str(uuid.uuid4)

    def get_absolute_url(self):
        return reverse('player_detail', args=[str(self.id)])

    def __str__(self):
        return self.slug

