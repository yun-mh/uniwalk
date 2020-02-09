from django import forms
from django.utils.translation import gettext_lazy as _
from localflavor.jp.forms import JPPostalCodeField
from phonenumber_field import formfields
from . import models


PAYMENT_CARD = "P1"
PAYMENT_TRANSFER = "P2"

PAYMENT_CHOICES = ((PAYMENT_CARD, _("クレジットカード")), (PAYMENT_TRANSFER, _("振込")))


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
        widgets = (
            {
                "last_name_recipient": forms.TextInput(attrs={"placeholder": _("姓")}),
                "first_name_recipient": forms.TextInput(attrs={"placeholder": _("名")}),
                "last_name_recipient_kana": forms.TextInput(
                    attrs={"placeholder": _("姓(カナ)")}
                ),
                "first_name_recipient_kana": forms.TextInput(
                    attrs={"placeholder": _("名(カナ)")}
                ),
                "phone_number_recipient": forms.TextInput(
                    attrs={"placeholder": _("電話番号")}
                ),
                "prefecture_recipient": forms.TextInput(
                    attrs={"placeholder": _("都道府県")}
                ),
                "address_city_recipient": forms.TextInput(
                    attrs={"placeholder": _("市区町村番地")}
                ),
                "address_detail_recipient": forms.TextInput(
                    attrs={"placeholder": _("建物名・号室")}
                ),
            },
        )

    last_name_recipient = forms.CharField(
        label=_("姓"), widget=forms.TextInput(attrs={"placeholder": _("姓")})
    )
    first_name_recipient = forms.CharField(
        label=_("名"), widget=forms.TextInput(attrs={"placeholder": _("名")})
    )
    last_name_recipient_kana = forms.CharField(
        label=_("姓(カナ)"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("姓(カナ)")}),
    )
    first_name_recipient_kana = forms.CharField(
        label=_("名(カナ)"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("名(カナ)")}),
    )
    phone_number_recipient = forms.CharField(
        label=_("電話番号"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("電話番号")}),
    )
    address_city_recipient = forms.CharField(
        label=_("市区町村番地"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("市区町村番地")}),
    )
    address_detail_recipient = forms.CharField(
        label=_("建物名・号室"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("建物名・号室")}),
    )
    postal_code_recipient = JPPostalCodeField(
        label=_("郵便番号"), 
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": _("郵便番号")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


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
        )
        widgets = {
            "payment": forms.RadioSelect(),
            "last_name_orderer": forms.TextInput(attrs={"placeholder": _("姓")}),
            "first_name_orderer": forms.TextInput(attrs={"placeholder": _("名")}),
            "last_name_orderer_kana": forms.TextInput(
                attrs={"placeholder": _("姓(カナ)")}
            ),
            "first_name_orderer_kana": forms.TextInput(
                attrs={"placeholder": _("名(カナ)")}
            ),
            "phone_number_orderer": forms.TextInput(attrs={"placeholder": _("電話番号")}),
            "postal_code_orderer": forms.TextInput(attrs={"placeholder": _("郵便番号")}),
            "address_city_orderer": forms.TextInput(attrs={"placeholder": _("市区町村番地")}),
            "address_detail_orderer": forms.TextInput(
                attrs={"placeholder": _("建物名・号室")}
            ),
        }

    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())
    last_name_orderer = forms.CharField(
        label=_("姓"), widget=forms.TextInput(attrs={"placeholder": _("姓")})
    )
    first_name_orderer = forms.CharField(
        label=_("名"), widget=forms.TextInput(attrs={"placeholder": _("名")})
    )
    last_name_orderer_kana = forms.CharField(
        label=_("姓(カナ)"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("姓(カナ)")}),
    )
    first_name_orderer_kana = forms.CharField(
        label=_("名(カナ)"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("名(カナ)")}),
    )
    phone_number_orderer = forms.CharField(
        label=_("電話番号"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("電話番号")}),
    )
    address_city_orderer = forms.CharField(
        label=_("市区町村番地"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("市区町村番地")}),
    )
    address_detail_orderer = forms.CharField(
        label=_("建物名・号室"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("建物名・号室")}),
    )
    postal_code_orderer = JPPostalCodeField(
        label=_("郵便番号"), 
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": _("郵便番号")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


class CardForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class OrderSearchForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = (
            "order_code",
            "email",
        )

    order_code = forms.CharField(
        label=_("注文番号"),
        widget=forms.TextInput(attrs={"placeholder": _("注文番号"), "required": True}),
    )
    email = forms.EmailField(
        label=_("メールアドレス"),
        widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス"), "required": True}),
    )

