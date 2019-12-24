from django import forms
from django.utils.translation import gettext_lazy as _
from localflavor.jp.forms import JPPostalCodeField
from phonenumber_field import formfields
from . import models


PAYMENT_CARD = "P1"
PAYMENT_TRANSFER = "P2"

PAYMENT_CHOICES = ((PAYMENT_CARD, "クレジットカード"), (PAYMENT_TRANSFER, "振込"))


class GuestForm(forms.Form):
    email = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス")})
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = (
            "last_name_recipient",
            "first_name_recipient",
            "last_name_recipient_kana",
            "first_name_recipient_kana",
            "phone_number_recipient",
            "postal_code_recipient",
            "prefecture_recipient",
            "address_city_recipient",
            "address_detail_recipient",
        )
        widgets = {
            "last_name_recipient": forms.TextInput(),
            "first_name_recipient": forms.TextInput(),
            "last_name_recipient_kana": forms.TextInput(),
            "first_name_recipient_kana": forms.TextInput(),
            "phone_number_recipient": forms.TextInput(),
            "prefecture_recipient": forms.TextInput(),
            "address_city_recipient": forms.TextInput(),
            "address_detail_recipient": forms.TextInput(),
        }
    
    last_name_recipient = forms.CharField(label=_(""), widget=forms.TextInput(attrs={"placeholder": _("")}))
    first_name_recipient = forms.CharField(label=_(""), widget=forms.TextInput(attrs={"placeholder": _("")}))
    last_name_recipient_kana = forms.CharField(label=_(""), required=True, widget=forms.TextInput(attrs={"placeholder": _("")}))
    first_name_recipient_kana = forms.CharField(label=_(""), required=True, widget=forms.TextInput(attrs={"placeholder": _("")}))
    phone_number_recipient = forms.CharField(label=_(""), required=True, widget=forms.TextInput(attrs={"placeholder": _("")}))
    prefecture_recipient = forms.CharField(label=_(""), required=True, widget=forms.TextInput(attrs={"placeholder": _("")}))
    address_city_recipient = forms.CharField(label=_(""), required=True, widget=forms.TextInput(attrs={"placeholder": _("")}))
    address_detail_recipient = forms.CharField(label=_(""), required=True, widget=forms.TextInput(attrs={"placeholder": _("")}))
    postal_code_recipient = JPPostalCodeField(
        label=_('郵便番号'),
        widget=forms.TextInput(attrs={"placeholder": _("郵便番号")}),
    )


class SelectPaymentForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = (
            "payment",
            "last_name_orderer",
            "first_name_orderer",
            "last_name_orderer_kana",
            "first_name_orderer_kana",
            "phone_number_orderer",
            "postal_code_orderer",
            "prefecture_orderer",
            "address_city_orderer",
            "address_detail_orderer",
            "is_same_with_recipient",
        )
        widgets = {
            "payment": forms.RadioSelect(),
            "last_name_orderer": forms.TextInput(),
            "first_name_orderer": forms.TextInput(),
            "last_name_orderer_kana": forms.TextInput(),
            "first_name_orderer_kana": forms.TextInput(),
            "phone_number_orderer": forms.TextInput(),
            "prefecture_orderer": forms.TextInput(),
            "address_city_orderer": forms.TextInput(),
            "address_detail_orderer": forms.TextInput(),
        }

    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())

    is_same_with_recipient = forms.BooleanField(
        label="請求書住所が配送先と同じ", initial=True, required=False, widget=forms.CheckboxInput()
    )

    # last_name_orderer = forms.TextInput()
    # first_name_orderer = forms.TextInput()
    # last_name_orderer_kana = forms.TextInput()
    # first_name_orderer_kana = forms.TextInput()
    # email = forms.EmailInput()
    # phone_number_orderer = forms.TextInput()
    # # postal_code_orderer = forms.TextInput()
    # prefecture_orderer = forms.TextInput()
    # address_city_orderer = forms.TextInput()
    # address_detail_orderer = forms.TextInput()
    # last_name_recipient = forms.TextInput()
    # first_name_recipient = forms.TextInput()
    # last_name_recipient_kana = forms.TextInput()
    # first_name_recipient_kana = forms.TextInput()
    # phone_number_recipient = forms.TextInput()
    # # postal_code_recipient = forms.TextInput()
    # prefecture_recipient = forms.TextInput()
    # address_city_recipient = forms.TextInput()
    # address_detail_recipient = forms.TextInput()
    # # payment
