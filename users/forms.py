from django import forms
from django.contrib.auth.views import PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード")})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError(_("パスワードをもう一度確認してください。")))
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
        )
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": _("メールアドレス")}),
            "last_name": forms.TextInput(attrs={"placeholder": _("姓")}),
            "first_name": forms.TextInput(attrs={"placeholder": _("名")}),
            "last_name_kana": forms.TextInput(attrs={"placeholder": _("姓(カナ)")}),
            "first_name_kana": forms.TextInput(attrs={"placeholder": _("名(カナ)")}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード")})
    )
    password1 = forms.CharField(
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
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        last_name = self.cleaned_data.get("last_name")
        first_name = self.cleaned_data.get("first_name")
        last_name_kana = self.cleaned_data.get("last_name_kana")
        first_name_kana = self.cleaned_data.get("first_name_kana")
        user.set_password(password)
        user.save()


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "email",
            "current_password",
            "new_password",
            "new_password1",
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
            "last_name": forms.TextInput(attrs={"placeholder": _("姓")}),
            "first_name": forms.TextInput(attrs={"placeholder": _("名")}),
            "last_name_kana": forms.TextInput(attrs={"placeholder": _("姓(カナ)")}),
            "first_name_kana": forms.TextInput(attrs={"placeholder": _("名(カナ)")}),
        }

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("現在のパスワード")}),
    )
    new_password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={"placeholder": _("新しいパスワード")}),
    )
    new_password1 = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={"placeholder": _("新しいパスワードの確認")}),
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        current_password = self.cleaned_data.get("current_password")
        user = models.User.objects.get(email=email)
        if user.check_password(current_password):
            return self.cleaned_data
        else:
            self.add_error("current_password", forms.ValidationError(_("パスワードをもう一度確認してください。")))

    def clean_new_password1(self):
        new_password = self.cleaned_data.get("new_password")
        new_password1 = self.cleaned_data.get("new_password1")

        if new_password != new_password1:
            raise forms.ValidationError(_("パスワードが一致しません。"))
        else:
            return new_password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        # email = self.cleaned_data.get("email")
        current_password = self.cleaned_data.get("current_password")
        new_password = self.cleaned_data.get("new_password")
        last_name = self.cleaned_data.get("last_name")
        first_name = self.cleaned_data.get("first_name")
        last_name_kana = self.cleaned_data.get("last_name_kana")
        first_name_kana = self.cleaned_data.get("first_name_kana")
        if len(new_password) > 0:
            user.set_password(new_password)
        return user


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


class WithdrawalForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("メールアドレス")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("パスワード")})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        user = models.User.objects.get(email=email)
        password = self.cleaned_data.get("password")
        if user.check_password(password):
            return self.cleaned_data
        else:
            self.add_error("password", forms.ValidationError(_("パスワードをもう一度確認してください。")))
