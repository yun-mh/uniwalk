from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from carts.models import Cart, CartItem


# セッションストアーのカスタマイズ
class SessionStore(DbSessionStore):
    def cycle_key(self):

        """ 非会員でカートにアイテムを登録時に、ログイン後でもカート情報を保持するための処理 """

        old_session_key = super(SessionStore, self).session_key
        super(SessionStore, self).cycle_key()
        self.save()
        Cart.objects.filter(session_key=old_session_key).update(
            session_key=self.session_key
        )

    def cycle_key_after_purchase(self):

        """ 商品購入後、ユーザのセッションキー情報を新しく更新させる """

        super(SessionStore, self).cycle_key()
        self.save()
