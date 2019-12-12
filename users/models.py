from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from core.models import JPPrefectureField, JPPostalCodeModelField
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.jp.jp_prefectures import JP_PREFECTURES

# Create your models here.
def create_member_number():
    last_member = User.objects.all().order_by("pk").last()
    if not last_member:
        return "0000001"
    member_number = last_member.member_number
    member_int = int(member_number)
    no_width = 7
    new_member_int = member_int + 1
    formatted = (no_width - len(str(new_member_int))) * '0' + str(new_member_int)
    new_member_number = str(formatted)
    return new_member_number


class User(AbstractUser):

    """ ユーザーのDBをカスタマイズする """

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_OTHER = "O"

    GENDER_CHOICES = ((GENDER_MALE, "男性"), (GENDER_FEMALE, "女性"), (GENDER_OTHER, "その他"))

    PREF_CHOICES = JP_PREFECTURES

    username = None

    email = models.EmailField(_("email address"), unique=True)
    first_name_kana = models.CharField("名(カナ)", blank=True, max_length=30)
    last_name_kana = models.CharField("姓(カナ)", blank=True, max_length=150)
    gender = models.CharField("性別", blank=True, choices=GENDER_CHOICES, max_length=10)
    birthday = models.DateField("生年月日", blank=True, null=True)
    phone_number = PhoneNumberField("電話番号", blank=True)
    postal_code = JPPostalCodeModelField("郵便番号")
    prefecture = JPPrefectureField("都道府県", blank=True)
    address_city = models.CharField("市区町村番地", max_length=40, blank=True)
    address_detail = models.CharField("建物名・号室", max_length=40, blank=True)
    member_number = models.CharField(
        max_length=40, default=create_member_number, blank=True, null=True
    )
    member_code = models.CharField(max_length=40, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_email_name(self):
        return self.email.split("@")[0]

    def get_absolute_url(self):
        return reverse("users:update-profile", kwargs={"pk": self.pk})
