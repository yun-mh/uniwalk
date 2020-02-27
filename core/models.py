from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from localflavor.jp.forms import JPPostalCodeField
from localflavor.jp.jp_prefectures import JP_PREFECTURE_CODES, JP_PREFECTURES


# 他アプリケーションに継承されるタイムスタンプモデルの定義
class TimeStampedModel(models.Model):

    """ 再利用可能なフィールドを各モデルに提供する """

    created = models.DateTimeField(_("登録日時"), auto_now_add=True)
    updated = models.DateTimeField(_("更新日時"), auto_now=True, null=True)

    class Meta:
        abstract = True


# 日本都道府県フィールドクラスの定義
class JPPrefectureField(CharField):

    """ データベースに都道府県のコード番号を入れるモデルフィールド """

    description = _("日本地域コード (2桁)")

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = JP_PREFECTURE_CODES
        kwargs["max_length"] = 2
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["choices"]
        return name, path, args, kwargs


# 日本郵便番号クラスの定義
class JPPostalCodeModelField(CharField):

    """ 日本郵便番号の７桁を入れるモデルフィールド """

    description = _("日本郵便番号：数字７桁")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 7
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"form_class": JPPostalCodeField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
