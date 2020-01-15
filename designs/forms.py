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
            "liner_color_left",
            "outsole_color_right",
            "midsole_color_right",
            "uppersole_color_right",
            "shoelace_color_right",
            "tongue_color_right",
            "liner_color_right",
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
        }

    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    # def save_screenshot(self):
    #     dataUrlPattern = re.compile("data:image/(png|jpeg);base64,(.*)$")
    #     image_data = self.cleaned_data.get("image_data")
    #     image_data = dataUrlPattern.match(image_data).group(2)
    #     image_data = image_data.encode()
    #     image_data = base64.b64decode(image_data)
    #     with open("screenshot.jpg", "wb") as f:
    #         f.write(image_data)
