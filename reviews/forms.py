from django import forms
from django.utils.translation import gettext_lazy as _
from products import models as product_models
from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            "title",
            "rate",
            "text",
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("レビュータイトル")}),
            "rate": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "text": forms.Textarea(attrs={"placeholder": _("レビュー本文")}),
        }

    def save(self, *args, **kwargs):
        review = super().save(commit=False)
        return review
