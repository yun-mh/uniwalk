from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class CustomizeForm(forms.ModelForm):
    class Meta:
        model = models.Design
        fields = (
            "outsole_color_left",
            "midsole_color_left",
            "uppersole_color_left",
            "shoelace_color_left",
            "tongue_color_left",
            "liner_color_left",
            "outsole_color_right",
            "midsole_color_right",
            "uppersole_color_right",
            "shoelace_color_right",
            "tongue_color_right",
            "liner_color_right",
        )
        widgets = {
            "outsole_color_left": forms.HiddenInput(),
            "midsole_color_left": forms.HiddenInput(),
            "uppersole_color_left": forms.HiddenInput(),
            "shoelace_color_left": forms.HiddenInput(),
            "tongue_color_left": forms.HiddenInput(),
            "liner_color_left": forms.HiddenInput(),
            "outsole_color_right": forms.HiddenInput(),
            "midsole_color_right": forms.HiddenInput(),
            "uppersole_color_right": forms.HiddenInput(),
            "shoelace_color_right": forms.HiddenInput(),
            "tongue_color_right": forms.HiddenInput(),
            "liner_color_right": forms.HiddenInput(),
        }