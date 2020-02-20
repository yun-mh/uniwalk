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


class FootsizeImageForm(forms.ModelForm):
    class Meta:
        model = models.FootImage
        fields = (
            "foot_left",
            "foot_right",
        )


class FootImageRotationForm(forms.Form):
    image_data_left = forms.CharField(widget=forms.HiddenInput(), required=False)
    image_data_right = forms.CharField(widget=forms.HiddenInput(), required=False)


class FootImageDataForm(forms.Form):
    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
