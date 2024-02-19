from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, View

from .models import Player


class RlistListView(ListView):

    model = Rlist

    template_name = "rlists/top800.html"

    def create_players(self, **kwargs):

        with Rlist.rlist_file as rlist_zip_file:

            with myzip.open(Rlist.rlist_filename) as rlist_unzippped_file:
                print("\n\n    class RlistView    \n\n")
                print("\n\n    create_players.rlist_unzippped_file.read()    \n\n")
                print(rlist_unzippped_file.read())

    def get_queryset(self, **kwargs):

        queryset = Player.objects.order_by("id")[:800]

        print("\n\n    queryset    \n\n")

        return queryset


class PlayerDetailView(DetailView):

    template_name = "rlists/player_detail.html"

    model = Player

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["player"] = get_object_or_404(Player, pk=self.kwargs["pk"])

        print("\n\n    class PlayerDetailView    \n\n")
        print("\n\n    get_context_data.context["player"]    \n\n")
        print(context["player"])

        return context

