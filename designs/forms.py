import re
import base64
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
            "outsole_color_right",
            "midsole_color_right",
            "uppersole_color_right",
            "shoelace_color_right",
            "tongue_color_right",
            "outsole_material_left",
            "midsole_material_left",
            "uppersole_material_left",
            "shoelace_material_left",
            "tongue_material_left",
            "outsole_material_right",
            "midsole_material_right",
            "uppersole_material_right",
            "shoelace_material_right",
            "tongue_material_right",
            "image_data",
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
            "outsole_material_left": forms.HiddenInput(),
            "midsole_material_left": forms.HiddenInput(),
            "uppersole_material_left": forms.HiddenInput(),
            "shoelace_material_left": forms.HiddenInput(),
            "tongue_material_left": forms.HiddenInput(),
            "liner_material_left": forms.HiddenInput(),
            "outsole_material_right": forms.HiddenInput(),
            "midsole_material_right": forms.HiddenInput(),
            "uppersole_material_right": forms.HiddenInput(),
            "shoelace_material_right": forms.HiddenInput(),
            "tongue_material_right": forms.HiddenInput(),
            "liner_material_right": forms.HiddenInput(),
        }

    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
