from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):

    """ ユーザーのDBをカスタマイズする """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "others"

    GENDER_CHOICES = ((GENDER_MALE, "男性"), (GENDER_FEMALE, "女性"), (GENDER_OTHER, "その他"))

    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name_kana = models.CharField("名(カナ)", blank=True, max_length=30)
    last_name_kana = models.CharField("姓(カナ)", blank=True, max_length=150)
    gender = models.CharField("性別", blank=True, choices=GENDER_CHOICES, max_length=10)
    birthday = models.DateField("生年月日", blank=True, null=True)
    phone_number = PhoneNumberField("電話番号", blank=True)
    postal_code = models.CharField("郵便番号", max_length=8, blank=True)
    prefecture = models.CharField(
        "都道府県", max_length=10, blank=True
    )  # yubinbango api 予定
    adress_city = models.CharField("市区町村番地", max_length=40, blank=True)
    adress_detail = models.CharField("建物名・号室", max_length=40, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
