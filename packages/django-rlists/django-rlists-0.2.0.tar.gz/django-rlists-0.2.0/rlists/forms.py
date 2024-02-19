from django import forms
from .models import Rlist


class RlistForm(forms.ModelForm):

    """
    https://stackoverflow.com/questions/9878475/django-modelform-override-widget
    """

    rating_list_file = forms.FileField(label = "")


    class Meta:

        model = Rlist

        fields = ["rating_list_file",]

