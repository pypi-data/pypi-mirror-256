from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.views.generic.base import TemplateView

from .views import PlayerDetailView, RlistListView


urlpatterns = [

    path("rlist/", RlistListView.as_view(), name='rlist_detail'),

    path("player/<int:pk>", PlayerDetailView.as_view(), name='player_detail'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

