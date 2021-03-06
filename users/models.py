from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from core.models import JPPrefectureField, JPPostalCodeModelField
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from core import models as core_models
from localflavor.jp.jp_prefectures import JP_PREFECTURES, JP_PREFECTURE_CODES
from datetime import date


# 会員番号の生成のための関数
def create_member_number():
    last_member = User.objects.all().order_by("pk").last()
    if not last_member:
        return "0000001"
    member_number = last_member.member_number
    member_int = int(member_number)
    no_width = 7
    new_member_int = member_int + 1
    formatted = (no_width - len(str(new_member_int))) * "0" + str(new_member_int)
    new_member_number = str(formatted)
    return new_member_number


class User(AbstractUser):

    """ ユーザーのDBをカスタマイズする """

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_OTHER = "O"

    GENDER_CHOICES = (
        ("", _("--性別--")),
        (GENDER_MALE, _("男性")),
        (GENDER_FEMALE, _("女性")),
        (GENDER_OTHER, _("その他")),
    )

    PREF_CHOICES = JP_PREFECTURES

    username = None

    email = models.EmailField(_("メールアドレス"), unique=True)
    first_name_kana = models.CharField(
        _("名(カナ)"),
        blank=True,
        max_length=30,
        validators=[
            RegexValidator(
                regex="[ア-ンー]", message=_("全角カタカナで入力してください。"), code="invalid",
            ),
        ],
    )
    last_name_kana = models.CharField(
        _("姓(カナ)"),
        blank=True,
        max_length=30,
        validators=[
            RegexValidator(
                regex="[ア-ンー]", message=_("全角カタカナで入力してください。"), code="invalid",
            ),
        ],
    )
    gender = models.CharField(
        _("性別"), blank=True, choices=GENDER_CHOICES, max_length=10
    )
    birthday = models.DateField(_("生年月日"), blank=True, null=True)
    phone_number = PhoneNumberField(_("電話番号"), blank=True, null=True)
    postal_code = JPPostalCodeModelField(_("郵便番号"), blank=True, null=True)
    prefecture = JPPrefectureField(_("都道府県"), blank=True, null=True)
    address_city = models.CharField(_("市区町村番地"), max_length=40, blank=True, null=True)
    address_detail = models.CharField(_("建物名・号室"), max_length=40, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    member_number = models.CharField(
        max_length=40, default=create_member_number, blank=True, null=True
    )
    member_code = models.CharField(_("会員番号"), max_length=40, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_email_name(self):
        return self.email.split("@")[0]

    def get_absolute_url(self):
        return reverse("users:update-profile")

    def calculate_age(self):
        today = date.today()
        try:
            age = (
                today.year
                - self.birthday.year
                - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            )
        except AttributeError:
            age = 0
        return age

    def save(self, *args, **kwargs):
        if self.is_staff == True or self.is_superuser == True:
            character = "S"
        else:
            character = "C"
        member_code = character + self.gender + self.member_number
        self.member_code = member_code
        super().save(*args, **kwargs)

    def as_dict(self):
        if self.prefecture is not None:
            prefecture_code = int(self.prefecture) - 1
            prefecture = JP_PREFECTURE_CODES[prefecture_code]
        if self.phone_number is not None:
            phone_number = self.phone_number.as_international
        else:
            phone_number = None

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "first_name_kana": self.first_name_kana,
            "last_name_kana": self.last_name_kana,
            "phone_number": phone_number,
            "postal_code": self.postal_code,
            "prefecture": self.prefecture,
            "address_city": self.address_city,
            "address_detail": self.address_detail,
        }


class Guest(core_models.TimeStampedModel):

    """ ゲストのモデルを定義する """

    email = models.EmailField(_("メールアドレス"), unique=True)
    active = models.BooleanField(_("活性化"), default=True)

    class Meta:
        verbose_name = _("ゲスト")
        verbose_name_plural = _("ゲスト")

    def __str__(self):
        return self.email
