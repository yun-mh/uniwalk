from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class FootsizeFillForm(forms.ModelForm):
    class Meta:
        model = models.Footsize
        fields = (
            "length_left",
            "length_right",
            "width_left",
            "width_right",
        )
