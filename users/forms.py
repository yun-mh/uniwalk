from django import forms
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
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "email",
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
