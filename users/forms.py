from django import forms
from django.contrib.auth.views import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from localflavor.jp.forms import JPPostalCodeField
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        label=_("メールアドレス"), widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス")})
    )
    password = forms.CharField(
        label=_("パスワード"), widget=forms.PasswordInput(attrs={"placeholder": _("パスワード")})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    "password", forms.ValidationError(_("パスワードをもう一度確認してください。"))
                )
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError(_("登録されていないメールアドレスです。")))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "email",
            "password",
            "password1",
            "last_name",
            "first_name",
            "last_name_kana",
            "first_name_kana",
            "gender",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={"placeholder": _("メールアドレス"), "required": True}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": _("姓"), "required": True}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": _("名"), "required": True}
            ),
            "last_name_kana": forms.TextInput(
                attrs={"placeholder": _("姓(カナ)"), "required": True}
            ),
            "first_name_kana": forms.TextInput(
                attrs={"placeholder": _("名(カナ)"), "required": True}
            ),
            "gender": forms.Select(attrs={"required": True}),
        }

    GENDER_CHOICES = (_("男性"), _("女性"), _("その他"))

    password = forms.CharField(
        label=_("パスワード"), widget=forms.PasswordInput(attrs={"placeholder": _("パスワード")})
    )
    password1 = forms.CharField(
        label=_("パスワード確認"),
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード確認")}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(_("既に登録されているメールアドレスです。"))
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError(_("パスワードが一致しません。"))
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "email",
            "current_password",
            "last_name",
            "first_name",
            "last_name_kana",
            "first_name_kana",
            "gender",
            "birthday",
            "phone_number",
            "postal_code",
            "prefecture",
            "address_city",
            "address_detail",
        )
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": _("メールアドレス")}),
            "current_password": forms.PasswordInput(
                attrs={"placeholder": _("現在のパスワード")}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": _("姓"), "required": True}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": _("名"), "required": True}
            ),
            "last_name_kana": forms.TextInput(
                attrs={"placeholder": _("姓(カナ)"), "required": True}
            ),
            "first_name_kana": forms.TextInput(
                attrs={"placeholder": _("名(カナ)"), "required": True}
            ),
            "birthday": forms.DateInput(
                attrs={"placeholder": _("生年月日"), "class": "datepicker"}
            ),
            "phone_number": forms.TextInput(attrs={"placeholder": _("電話番号")}),
            "address_city": forms.TextInput(attrs={"placeholder": _("市区町村番地")}),
            "address_detail": forms.TextInput(attrs={"placeholder": _("建物名・号室")}),
        }

    current_password = forms.CharField(
        label=_("現在のパスワード"),
        widget=forms.PasswordInput(attrs={"placeholder": _("現在のパスワード")}),
    )

    postal_code = JPPostalCodeField(
        label=_("郵便番号"), widget=forms.TextInput(attrs={"placeholder": _("郵便番号")}),
    )

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields["gender"].empty_label = ""

    def clean(self):
        email = self.cleaned_data.get("email")
        current_password = self.cleaned_data.get("current_password")
        user = models.User.objects.get(email=email)
        if user.check_password(current_password):
            return self.cleaned_data
        else:
            self.add_error(
                "current_password", forms.ValidationError(_("パスワードをもう一度確認してください。"))
            )

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        return user


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("現在パスワード")}),
    )
    new_password1 = forms.CharField(
        label=_("new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("新しいパスワード")}),
    )
    new_password2 = forms.CharField(
        label=_("check password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード確認")}),
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス")}),
        label=_("Email"),
        max_length=254,
    )


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("新しいパスワード"),
        widget=forms.PasswordInput(attrs={"placeholder": _("新しいパスワード")}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("パスワード確認"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード確認")}),
    )


class AddCardForm(forms.Form):
    stripeToken = forms.CharField(required=False)


class WithdrawalForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード")})
    )

