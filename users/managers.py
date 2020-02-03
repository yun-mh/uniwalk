from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    """
    ユーザネームの代わりにメールアドレスを会員を特定できるユニーク値としてカスタムユーザモデルを生成
    """

    def create_user(self, email, password, **extra_fields):

        """
        一般ユーザ作成用
        """

        if not email:
            raise ValueError(_("メールアドレスを入力してください。"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        """
        スーパーユーザ作成用
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("スーパーユーザにはスタフ権限が必須です。"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("スーパーユーザにはスーパーユーザ権限が必須です。"))
        return self.create_user(email, password, **extra_fields)
