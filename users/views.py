from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    View,
    FormView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
    TemplateView,
)
from cards import models as card_models
from carts import models as cart_models
from designs import forms as design_forms
from designs import models as design_models
from feet import models as feet_models
from feet import forms as feet_forms
from feet import analyze
from orders import models as order_models
from products import models as product_models
from . import forms, models, mixins
import stripe, base64, json


stripe.api_key = settings.STRIPE_SECRET_KEY

# インコードした画像データを画像にデコードする関数
def base64_file(data, name=None):
    _format, _img_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    result = ContentFile(base64.b64decode(_img_str), name="{}.{}".format(name, ext))
    return result


class LoginView(mixins.LoggedOutOnlyView, FormView):

    """ ログイン """

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            session_key = self.request.session.session_key
            cart_models.Cart.objects.filter(session_key=session_key).update(
                user_id=self.request.user.pk
            )
            messages.success(self.request, _("ログインしました。"))
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):

    """ ログアウト """

    messages.info(request, _("ログアウトしました。"))
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    """ 会員登録 """

    template_name = "users/signup.html"
    form_class = forms.SignUpForm

    def get_initial(self):
        if self.request.session.get("data"):
            return self.request.session["data"]
        else:
            return self.initial.copy()

    def form_valid(self, user):
        data = {
            "email": user.cleaned_data.get("email"),
            "password": user.cleaned_data.get("password"),
            "last_name": user.cleaned_data.get("last_name"),
            "first_name": user.cleaned_data.get("first_name"),
            "last_name_kana": user.cleaned_data.get("last_name_kana"),
            "first_name_kana": user.cleaned_data.get("first_name_kana"),
            "gender": user.cleaned_data.get("gender"),
        }
        self.request.session["data"] = data
        return redirect(reverse("users:signup-check"))


class SignUpCheckView(mixins.LoggedOutOnlyView, FormView):

    """ 会員登録情報確認 """

    template_name = "users/signup-check.html"

    def get(self, request):
        data = request.session.get("data")
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = request.session.get("data")
        user = models.User.objects.create(
            email=data["email"],
            last_name=data["last_name"],
            first_name=data["first_name"],
            last_name_kana=data["last_name_kana"],
            first_name_kana=data["first_name_kana"],
            gender=data["gender"],
        )
        user.set_password(data["password"])
        user.save()
        email = data["email"]
        html_message = render_to_string("emails/registration-done.html")
        send_mail(
            _("Uniwalk 会員登録ありがとうございます。"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        del request.session["data"]
        return redirect(reverse("users:signup-success"))


class SignupSuccessView(mixins.LoggedOutOnlyView, View):

    """ 会員登録完了 """

    def get(self, request):
        return render(request, "users/signup-success.html")


class PasswordResetView(PasswordResetView):

    """ パスワード再設定申し込み """

    form_class = forms.PasswordResetForm
    template_name = "users/password-reset.html"
    subject_template_name = "emails/password-reset-subject.txt"
    email_template_name = "emails/password_reset_form.html"
    html_email_template_name = "emails/password_reset_form.html"
    success_url = reverse_lazy("users:password-reset-done")


class PasswordResetDoneView(PasswordResetDoneView):

    """ パスワード再設定申し込み完了 """

    template_name = "users/password-reset-done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):

    """ パスワード再設定 """

    form_class = forms.SetPasswordForm
    template_name = "users/password-reset-confirm.html"
    success_url = reverse_lazy("users:password-reset-complete")

    def form_valid(self, form):
        email = self.user.email
        html_message = render_to_string("emails/password-reset-done.html")
        send_mail(
            _("Uniwalk パスワード再設定完了のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class PasswordResetCompleteView(PasswordResetCompleteView):

    """ パスワード再設定完了 """

    template_name = "users/password-reset-complete.html"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    """ 会員登録情報変更 """

    form_class = forms.UpdateProfileForm
    template_name = "users/update-profile.html"
    success_message = _("会員情報を変更しました。")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:update-profile")

    def form_valid(self, form):
        user = form.save()
        user.save()
        email = form.cleaned_data.get("email")
        html_message = render_to_string("emails/profile-change-done.html")
        send_mail(
            _("Uniwalk 会員情報変更のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class PasswordChangeView(mixins.LoggedInOnlyView, PasswordChangeView):

    """ パスワード変更 """

    form_class = forms.PasswordChangeForm
    template_name = "users/password-change.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        email = self.request.user.email
        html_message = render_to_string("emails/password-change-done.html")
        send_mail(
            _("UniWalk パスワード変更のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, _("パスワードを変更しました。"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("users:update-profile")


class OrdersListView(mixins.LoggedInOnlyView, ListView):

    """ 注文履歴 """

    model = order_models.Order
    template_name = "orders/order-list.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        try:
            return order_models.Order.objects.filter(
                user_id=self.request.user.pk
            ).order_by("-order_date")
        except order_models.Order.DoesNotExist:
            return None

    def post(self, *args, **kwargs):
        order_pk = self.request.POST.get("target-order")
        target = order_models.Order.objects.filter(pk=order_pk)
        cancel = order_models.Step.objects.get(step_code="T99")
        target.update(step=cancel)
        email = self.request.user.email
        html_message = render_to_string(
            "emails/cancel-done.html",
            {"order_code": order_models.Order.objects.get(pk=order_pk).order_code},
        )
        send_mail(
            _("Uniwalk ご注文取消しのご連絡"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        messages.success(self.request, _("注文を取消しました。"))
        return redirect("users:orders")


class OrdersDetailView(mixins.LoggedInOnlyView, DetailView):

    """ 注文詳細 """

    model = order_models.Order
    template_name = "orders/order-detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_pk"

    def get(self, request, *args, **kwargs):
        try:
            return super(OrdersDetailView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            # messages.error(request, _("アクセスできません。"))
            return redirect("users:orders")

    def get_object(self):
        return order_models.Order.objects.filter(user_id=self.request.user.pk).get(
            pk=self.kwargs.get("order_pk")
        )

    def post(self, *args, **kwargs):
        order_pk = self.request.POST.get("target-order")
        target = order_models.Order.objects.filter(pk=order_pk)
        cancel = order_models.Step.objects.get(step_code="T99")
        target.update(step=cancel)
        email = self.request.user.email
        html_message = render_to_string(
            "emails/cancel-done.html",
            {"order_code": order_models.Order.objects.get(pk=order_pk).order_code},
        )
        send_mail(
            _("Uniwalk ご注文取消しのご連絡"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        messages.success(self.request, _("注文を取消しました。"))
        return redirect("users:orders")


class CardsListView(mixins.LoggedInOnlyView, FormView):

    """ クレジットカードリスト """

    def get(self, *args, **kwargs):
        # ページ化
        page = self.request.GET.get("page")
        user = self.request.user
        try:
            cards = stripe.Customer.list_sources(user.stripe_customer_id, object="card")
        except:
            cards = {"data": []}
        card_list = cards["data"]
        paginator = Paginator(card_list, 2)
        items = paginator.get_page(page)
        context = {}
        if len(card_list) > 0:
            context = {
                "cards": items,
            }
        return render(self.request, "cards/card-list.html", context)

    def post(self, *args, **kwargs):
        card_customer = self.request.POST.get("target-customer")
        card_id = self.request.POST.get("target-card")
        card_fingerprint = self.request.POST.get("target-fingerprint")
        stripe.Customer.delete_source(
            card_customer, card_id,
        )
        target = card_models.Card.objects.get(
            stripe_customer_id=card_customer, fingerprint=card_fingerprint,
        )
        target.delete()
        messages.success(self.request, _("カードを登録解除しました。"))
        return redirect("users:cards")


class CardsAddView(mixins.LoggedInOnlyView, View):

    """ クレジットカード登録 """

    def get(self, *args, **kwargs):
        # user = self.request.user
        add_card_form = forms.AddCardForm()
        context = {"add_card_form": add_card_form}
        return render(self.request, "cards/card-registration.html", context)

    def post(self, *args, **kwargs):
        add_card_form = forms.AddCardForm(self.request.POST)
        if add_card_form.is_valid():
            user = models.User.objects.get(email=self.request.user)
            token = add_card_form.cleaned_data.get("stripeToken")
            # ユーザにstripe_customer_idが存在する場合
            if user.stripe_customer_id != "" and user.stripe_customer_id is not None:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
                card_id = stripe.Token.retrieve(token).card.id
                current_fingerprint = stripe.Token.retrieve(token).card.fingerprint
                current_exp_month = stripe.Token.retrieve(token).card.exp_month
                current_exp_year = stripe.Token.retrieve(token).card.exp_year
                # カードテーブルからデータを取得してみる
                try:
                    card_models.Card.objects.get(
                        fingerprint=current_fingerprint,
                        exp_month=current_exp_month,
                        exp_year=current_exp_year,
                    )
                    messages.error(self.request, _("既に登録されているカードです。"))
                    return redirect(reverse("users:cards"))
                # カードテーブルにデータが存在しない場合、データを入れる
                except card_models.Card.DoesNotExist:
                    customer.sources.create(card=token)
                    card_models.Card.objects.create(
                        stripe_customer_id=user.stripe_customer_id,
                        card_id=card_id,
                        fingerprint=current_fingerprint,
                        exp_month=current_exp_month,
                        exp_year=current_exp_year,
                    )
                    messages.success(self.request, _("カードを登録しました。"))
                    return redirect("users:cards")
            # ユーザにstripe_customer_idが存在しない場合
            else:
                card_id = stripe.Token.retrieve(token).card.id
                current_fingerprint = stripe.Token.retrieve(token).card.fingerprint
                current_exp_month = stripe.Token.retrieve(token).card.exp_month
                current_exp_year = stripe.Token.retrieve(token).card.exp_year
                customer = stripe.Customer.create(email=self.request.user.email,)
                user.stripe_customer_id = customer["id"]
                user.save()
                customer.sources.create(card=token)
                card_models.Card.objects.create(
                    stripe_customer_id=user.stripe_customer_id,
                    card_id=card_id,
                    fingerprint=current_fingerprint,
                    exp_month=current_exp_month,
                    exp_year=current_exp_year,
                )
                messages.success(self.request, _("カードを登録しました。"))
                return redirect("users:cards")
        else:
            messages.error(self.request, _("カード登録に失敗しました。"))
            return redirect(reverse("users:add-card"))


class MyDesignsListView(mixins.LoggedInOnlyView, ListView):

    """ マイデザインリスト """

    model = design_models.Design
    template_name = "designs/design-list.html"
    context_object_name = "designs"
    paginate_by = 5

    def get_queryset(self):
        try:
            return design_models.Design.objects.filter(
                user_id=self.request.user.pk
            ).order_by("-created")
        except design_models.Design.DoesNotExist:
            return None

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            if "design_delete" in self.request.POST:
                design_id = self.request.POST.get("target-design-delete")
                design_models.Design.objects.get(pk=design_id).delete()
                messages.success(self.request, _("デザインを削除しました。"))
                return redirect("users:mydesigns")
            elif "design_modify" in self.request.POST:
                design_id = self.request.POST.get("target-design-modify")
                design = design_models.Design.objects.get(pk=design_id)
                design_image = design_models.Image.objects.get(design=design)
                product = product_models.Product.objects.get(pk=design.product.pk)
                self.request.session["product"] = product.pk
                self.request.session["design"] = design.pk
                self.request.session["design_image"] = design_image.pk
                return redirect("users:modify")


class SelectProductToCustomizeView(mixins.LoggedInOnlyView, ListView):

    """ マイページでデザインカスタマイズする場合対象商品を選択するためのビュー """

    model = product_models.Product
    template_name = "designs/select-products.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        return product_models.Product.objects.all().order_by("-created")


class MemberCustomizeView(mixins.LoggedInOnlyView, ListView):

    """ 会員用デザインカスタマイズ """

    model = design_models.Design
    template_name = "designs/design-customize.html"
    context_object_name = "designs"
    paginate_by = 5

    def get_template_names(self):
        if self.request.is_ajax():
            return ["mixins/designs/related_design_card.html"]
        return super(MemberCustomizeView, self).get_template_names()

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        designs = (
            design_models.Design.objects.filter(product=pk)
            .exclude(user__isnull=True)
            .all()
        )
        return sorted(designs, key=lambda design: design.total_likes, reverse=True)

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        materials = design_models.Material.objects.all().order_by("created")
        context = super(MemberCustomizeView, self).get_context_data(*args, **kwargs)
        for material in materials:
            context["mat" + str(material.pk)] = material
        context["product"] = product_models.Product.objects.get(pk=pk)
        context["template"] = product_models.Template.objects.get(product=pk)
        context["form"] = design_forms.CustomizeForm()
        return context

    def post(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        customize_form = design_forms.CustomizeForm(self.request.POST)
        customize_data = {
            "outsole_color_left": self.request.POST.get("outsole_color_left"),
            "midsole_color_left": self.request.POST.get("midsole_color_left"),
            "uppersole_color_left": self.request.POST.get("uppersole_color_left"),
            "shoelace_color_left": self.request.POST.get("shoelace_color_left"),
            "tongue_color_left": self.request.POST.get("tongue_color_left"),
            "outsole_color_right": self.request.POST.get("outsole_color_right"),
            "midsole_color_right": self.request.POST.get("midsole_color_right"),
            "uppersole_color_right": self.request.POST.get("uppersole_color_right"),
            "shoelace_color_right": self.request.POST.get("shoelace_color_right"),
            "tongue_color_right": self.request.POST.get("tongue_color_right"),
            "outsole_material_left": self.request.POST.get("outsole_material_left"),
            "midsole_material_left": self.request.POST.get("midsole_material_left"),
            "uppersole_material_left": self.request.POST.get("uppersole_material_left"),
            "shoelace_material_left": self.request.POST.get("shoelace_material_left"),
            "tongue_material_left": self.request.POST.get("tongue_material_left"),
            "outsole_material_right": self.request.POST.get("outsole_material_right"),
            "midsole_material_right": self.request.POST.get("midsole_material_right"),
            "uppersole_material_right": self.request.POST.get(
                "uppersole_material_right"
            ),
            "shoelace_material_right": self.request.POST.get("shoelace_material_right"),
            "tongue_material_right": self.request.POST.get("tongue_material_right"),
        }
        if self.request.user.is_authenticated:
            user = self.request.user
            new_design = design_models.Design.objects.create(
                user=user,
                product=product_models.Product.objects.get(pk=pk),
                outsole_color_left=customize_data["outsole_color_left"],
                midsole_color_left=customize_data["midsole_color_left"],
                uppersole_color_left=customize_data["uppersole_color_left"],
                shoelace_color_left=customize_data["shoelace_color_left"],
                tongue_color_left=customize_data["tongue_color_left"],
                outsole_color_right=customize_data["outsole_color_right"],
                midsole_color_right=customize_data["midsole_color_right"],
                uppersole_color_right=customize_data["uppersole_color_right"],
                shoelace_color_right=customize_data["shoelace_color_right"],
                tongue_color_right=customize_data["tongue_color_right"],
                outsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_left"]
                ),
                midsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_left"]
                ),
                uppersole_material_left=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_left"]
                ),
                shoelace_material_left=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_left"]
                ),
                tongue_material_left=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_left"]
                ),
                outsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_right"]
                ),
                midsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_right"]
                ),
                uppersole_material_right=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_right"]
                ),
                shoelace_material_right=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_right"]
                ),
                tongue_material_right=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_right"]
                ),
            )
        else:
            new_design = design_models.Design.objects.create(
                product=product_models.Product.objects.get(pk=pk),
                outsole_color_left=customize_data["outsole_color_left"],
                midsole_color_left=customize_data["midsole_color_left"],
                uppersole_color_left=customize_data["uppersole_color_left"],
                shoelace_color_left=customize_data["shoelace_color_left"],
                tongue_color_left=customize_data["tongue_color_left"],
                outsole_color_right=customize_data["outsole_color_right"],
                midsole_color_right=customize_data["midsole_color_right"],
                uppersole_color_right=customize_data["uppersole_color_right"],
                shoelace_color_right=customize_data["shoelace_color_right"],
                tongue_color_right=customize_data["tongue_color_right"],
                outsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_left"]
                ),
                midsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_left"]
                ),
                uppersole_material_left=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_left"]
                ),
                shoelace_material_left=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_left"]
                ),
                tongue_material_left=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_left"]
                ),
                outsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_right"]
                ),
                midsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_right"]
                ),
                uppersole_material_right=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_right"]
                ),
                shoelace_material_right=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_right"]
                ),
                tongue_material_right=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_right"]
                ),
            )

        # 画像情報をデータベースに反映する
        image_data_front = self.request.POST.get("image_data_front")
        image_data_side = self.request.POST.get("image_data_side")
        image_data_up = self.request.POST.get("image_data_up")
        image_data_down = self.request.POST.get("image_data_down")
        design_models.Image.objects.create(
            design=new_design,
            front=base64_file(image_data_front),
            side=base64_file(image_data_side),
            up=base64_file(image_data_up),
            down=base64_file(image_data_down),
        )
        return redirect("users:mydesigns")


def get_palette(request):

    """ 参照用デザインパレットを呼び出すビュー """

    if request.method == "POST" and request.is_ajax():
        outsole_color_left = request.POST.get("outsole_color_left")
        midsole_color_left = request.POST.get("midsole_color_left")
        uppersole_color_left = request.POST.get("uppersole_color_left")
        shoelace_color_left = request.POST.get("shoelace_color_left")
        tongue_color_left = request.POST.get("tongue_color_left")
        outsole_color_right = request.POST.get("outsole_color_right")
        midsole_color_right = request.POST.get("midsole_color_right")
        uppersole_color_right = request.POST.get("uppersole_color_right")
        shoelace_color_right = request.POST.get("shoelace_color_right")
        tongue_color_right = request.POST.get("tongue_color_right")
        outsole_material_left = design_models.Material.objects.get(
            pk=request.POST.get("outsole_material_left")
        ).file.url
        midsole_material_left = design_models.Material.objects.get(
            pk=request.POST.get("midsole_material_left")
        ).file.url
        uppersole_material_left = design_models.Material.objects.get(
            pk=request.POST.get("uppersole_material_left")
        ).file.url
        shoelace_material_left = design_models.Material.objects.get(
            pk=request.POST.get("shoelace_material_left")
        ).file.url
        tongue_material_left = design_models.Material.objects.get(
            pk=request.POST.get("tongue_material_left")
        ).file.url
        outsole_material_right = design_models.Material.objects.get(
            pk=request.POST.get("outsole_material_right")
        ).file.url
        midsole_material_right = design_models.Material.objects.get(
            pk=request.POST.get("midsole_material_right")
        ).file.url
        uppersole_material_right = design_models.Material.objects.get(
            pk=request.POST.get("uppersole_material_right")
        ).file.url
        shoelace_material_right = design_models.Material.objects.get(
            pk=request.POST.get("shoelace_material_right")
        ).file.url
        tongue_material_right = design_models.Material.objects.get(
            pk=request.POST.get("tongue_material_right")
        ).file.url
        response = json.dumps(
            {
                "outsole_color_left": outsole_color_left,
                "midsole_color_left": midsole_color_left,
                "uppersole_color_left": uppersole_color_left,
                "shoelace_color_left": shoelace_color_left,
                "tongue_color_left": tongue_color_left,
                "outsole_color_right": outsole_color_right,
                "midsole_color_right": midsole_color_right,
                "uppersole_color_right": uppersole_color_right,
                "shoelace_color_right": shoelace_color_right,
                "tongue_color_right": tongue_color_right,
                "outsole_material_left": outsole_material_left,
                "midsole_material_left": midsole_material_left,
                "uppersole_material_left": uppersole_material_left,
                "shoelace_material_left": shoelace_material_left,
                "tongue_material_left": tongue_material_left,
                "outsole_material_right": outsole_material_right,
                "midsole_material_right": midsole_material_right,
                "uppersole_material_right": uppersole_material_right,
                "shoelace_material_right": shoelace_material_right,
                "tongue_material_right": tongue_material_right,
            }
        )
        return HttpResponse(response, content_type="application/json")
    else:
        raise Http404


class MemberCustomizeModifyView(mixins.LoggedInOnlyView, ListView):

    """ 会員用デザインカスタマイズ修正ビュー """

    model = design_models.Design
    template_name = "designs/design-customize.html"
    context_object_name = "designs"
    paginate_by = 5

    def get_template_names(self):
        if self.request.is_ajax():
            return ["mixins/designs/related_design_card.html"]
        return super(MemberCustomizeModifyView, self).get_template_names()

    def get_queryset(self):
        pk = self.request.session["product"]
        designs = (
            design_models.Design.objects.filter(product=pk)
            .exclude(user__isnull=True)
            .all()
        )
        return sorted(designs, key=lambda design: design.total_likes, reverse=True)

    def get_context_data(self, *args, **kwargs):
        pk = self.request.session["product"]
        design_pk = self.request.session["design"]
        materials = design_models.Material.objects.all().order_by("created")
        design_before = design_models.Design.objects.get(pk=design_pk)
        context = super(MemberCustomizeModifyView, self).get_context_data(
            *args, **kwargs
        )
        for material in materials:
            context["mat" + str(material.pk)] = material
        context["design_before"] = design_before
        context["product"] = product_models.Product.objects.get(pk=pk)
        context["template"] = product_models.Template.objects.get(product=pk)
        context["form"] = design_forms.CustomizeForm()
        return context

    def post(self, *args, **kwargs):
        pk = self.request.session["product"]
        design_pk = self.request.session["design"]
        design_image_pk = self.request.session["design_image"]
        customize_form = design_forms.CustomizeForm(self.request.POST)
        customize_data = {
            "outsole_color_left": self.request.POST.get("outsole_color_left"),
            "midsole_color_left": self.request.POST.get("midsole_color_left"),
            "uppersole_color_left": self.request.POST.get("uppersole_color_left"),
            "shoelace_color_left": self.request.POST.get("shoelace_color_left"),
            "tongue_color_left": self.request.POST.get("tongue_color_left"),
            "outsole_color_right": self.request.POST.get("outsole_color_right"),
            "midsole_color_right": self.request.POST.get("midsole_color_right"),
            "uppersole_color_right": self.request.POST.get("uppersole_color_right"),
            "shoelace_color_right": self.request.POST.get("shoelace_color_right"),
            "tongue_color_right": self.request.POST.get("tongue_color_right"),
            "outsole_material_left": self.request.POST.get("outsole_material_left"),
            "midsole_material_left": self.request.POST.get("midsole_material_left"),
            "uppersole_material_left": self.request.POST.get("uppersole_material_left"),
            "shoelace_material_left": self.request.POST.get("shoelace_material_left"),
            "tongue_material_left": self.request.POST.get("tongue_material_left"),
            "outsole_material_right": self.request.POST.get("outsole_material_right"),
            "midsole_material_right": self.request.POST.get("midsole_material_right"),
            "uppersole_material_right": self.request.POST.get(
                "uppersole_material_right"
            ),
            "shoelace_material_right": self.request.POST.get("shoelace_material_right"),
            "tongue_material_right": self.request.POST.get("tongue_material_right"),
        }
        if self.request.user.is_authenticated:
            design_models.Design.objects.filter(pk=design_pk).update(
                product=product_models.Product.objects.get(pk=pk),
                outsole_color_left=customize_data["outsole_color_left"],
                midsole_color_left=customize_data["midsole_color_left"],
                uppersole_color_left=customize_data["uppersole_color_left"],
                shoelace_color_left=customize_data["shoelace_color_left"],
                tongue_color_left=customize_data["tongue_color_left"],
                outsole_color_right=customize_data["outsole_color_right"],
                midsole_color_right=customize_data["midsole_color_right"],
                uppersole_color_right=customize_data["uppersole_color_right"],
                shoelace_color_right=customize_data["shoelace_color_right"],
                tongue_color_right=customize_data["tongue_color_right"],
                outsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_left"]
                ),
                midsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_left"]
                ),
                uppersole_material_left=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_left"]
                ),
                shoelace_material_left=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_left"]
                ),
                tongue_material_left=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_left"]
                ),
                outsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_right"]
                ),
                midsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_right"]
                ),
                uppersole_material_right=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_right"]
                ),
                shoelace_material_right=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_right"]
                ),
                tongue_material_right=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_right"]
                ),
            )
        else:
            design_models.Design.objects.filter(pk=design_pk).update(
                product=product_models.Product.objects.get(pk=pk),
                outsole_color_left=customize_data["outsole_color_left"],
                midsole_color_left=customize_data["midsole_color_left"],
                uppersole_color_left=customize_data["uppersole_color_left"],
                shoelace_color_left=customize_data["shoelace_color_left"],
                tongue_color_left=customize_data["tongue_color_left"],
                outsole_color_right=customize_data["outsole_color_right"],
                midsole_color_right=customize_data["midsole_color_right"],
                uppersole_color_right=customize_data["uppersole_color_right"],
                shoelace_color_right=customize_data["shoelace_color_right"],
                tongue_color_right=customize_data["tongue_color_right"],
                outsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_left"]
                ),
                midsole_material_left=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_left"]
                ),
                uppersole_material_left=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_left"]
                ),
                shoelace_material_left=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_left"]
                ),
                tongue_material_left=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_left"]
                ),
                outsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["outsole_material_right"]
                ),
                midsole_material_right=design_models.Material.objects.get(
                    pk=customize_data["midsole_material_right"]
                ),
                uppersole_material_right=design_models.Material.objects.get(
                    pk=customize_data["uppersole_material_right"]
                ),
                shoelace_material_right=design_models.Material.objects.get(
                    pk=customize_data["shoelace_material_right"]
                ),
                tongue_material_right=design_models.Material.objects.get(
                    pk=customize_data["tongue_material_right"]
                ),
            )

        # 画像情報をデータベースに反映する
        image_data_front = base64_file(self.request.POST.get("image_data_front"))
        image_data_side = base64_file(self.request.POST.get("image_data_side"))
        image_data_up = base64_file(self.request.POST.get("image_data_up"))
        image_data_down = base64_file(self.request.POST.get("image_data_down"))
        modify_target = design_models.Image.objects.get(pk=design_image_pk)
        modify_target.front = image_data_front
        modify_target.side = image_data_side
        modify_target.up = image_data_up
        modify_target.down = image_data_down
        modify_target.save()

        # セッションの値を初期化する
        del self.request.session["product"]
        del self.request.session["design"]
        del self.request.session["design_image"]
        return redirect("users:mydesigns")


class FootSizeView(mixins.LoggedInOnlyView, ListView):

    """ マイ足サイズ確認ビュー """

    model = feet_models.Footsize
    template_name = "feet/feet-list.html"
    context_object_name = "feet"

    def get_queryset(self):
        try:
            return feet_models.Footsize.objects.get(user_id=self.request.user.pk)
        except feet_models.Footsize.DoesNotExist:
            return None


@login_required()
def footsizes_measure(request, *args, **kwargs):

    """ 足サイズ測定 """

    # 足測定の結果をデータベースに反映する
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
        # 記入式で足サイズを指定した場合
        if "footsize-fill" in request.POST:
            footsize_fill_form = feet_forms.FootsizeFillForm(
                request.POST, prefix="fill"
            )
            if footsize_fill_form.is_valid():
                length_left = footsize_fill_form.cleaned_data.get("length_left")
                width_left = footsize_fill_form.cleaned_data.get("width_left")
                length_right = footsize_fill_form.cleaned_data.get("length_right")
                width_right = footsize_fill_form.cleaned_data.get("width_right")
                # 会員に既存の足サイズデータがある場合、データを更新する
                try:
                    footsize = feet_models.Footsize.objects.get(user=user)
                    footsize.length_left = length_left
                    footsize.length_right = length_right
                    footsize.width_left = width_left
                    footsize.width_right = width_right
                    footsize.save()
                # 会員に足サイズデータが存在しない場合、データを新規登録する
                except feet_models.Footsize.DoesNotExist:
                    footsize = feet_models.Footsize.objects.create(
                        user=user,
                        length_left=length_left,
                        length_right=length_right,
                        width_left=width_left,
                        width_right=width_right,
                    )
                # カートに登録している他商品の足サイズと区分するためにセッションで足サイズを渡す
                request.session["length_left"] = int(length_left)
                request.session["length_right"] = int(length_right)
                request.session["width_left"] = int(width_left)
                request.session["width_right"] = int(width_right)
                # 登録完了のメッセージを表示し、元の画面に戻る
                messages.success(request, _("足サイズを登録しました。"))
                return redirect("users:footsizes")
            else:
                messages.error(request, _("入力した情報をもう一度確認してください。"))
            footsize_image_form = feet_forms.FootsizeImageForm(prefix="image")
        # イメージ測定を選んだ場合
        elif "footsize-image" in request.POST:
            footsize_image_form = feet_forms.FootsizeImageForm(
                request.POST, request.FILES, prefix="image"
            )
            if footsize_image_form.is_valid():
                foot_images = feet_models.FootImage(
                    foot_left=request.FILES["image-foot_left"],
                    foot_right=request.FILES["image-foot_right"],
                )
                foot_images.save()
                request.session["foot_images"] = foot_images.pk
                return redirect("users:rotation")
            footsize_fill_form = feet_forms.FootsizeFillForm(prefix="fill")
    else:
        footsize_fill_form = feet_forms.FootsizeFillForm(prefix="fill")
        footsize_image_form = feet_forms.FootsizeImageForm(prefix="image")
    context = {
        "footsize_fill_form": footsize_fill_form,
        "footsize_image_form": footsize_image_form,
    }
    return render(request, "feet/feet-measure.html", context)


class FootImageRotationView(mixins.LoggedInOnlyView, DetailView):

    """ 足イメージをローテートするためのツールを提供する """

    model = feet_models.FootImage
    context_object_name = "foot_images"
    template_name = "feet/feet-rotation.html"

    def get(self, request, *args, **kwargs):
        try:
            foot = self.request.session["foot_images"]
        except KeyError:
            messages.error(self.request, _("問題が発生しました。もう一度試してみてください。"))
            return redirect(reverse("users:footsizes"))
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return feet_models.FootImage.objects.get(
                pk=self.request.session["foot_images"]
            )
        except KeyError:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = feet_forms.FootImageRotationForm()
        return context

    def post(self, *args, **kwargs):
        feet = feet_models.FootImage.objects.get(pk=self.request.session["foot_images"])
        # 画像情報をデータベースに反映する
        image_data_left = self.request.POST.get("image_data_left")
        image_data_right = self.request.POST.get("image_data_right")
        feet.foot_left = base64_file(image_data_left)
        feet.foot_right = base64_file(image_data_right)
        feet.save()
        return redirect("users:crop-left")


class LeftFootsizePerspeciveCropperView(mixins.LoggedInOnlyView, DetailView):

    """ 左足のイメージをクロップするためのツールを提供する """

    model = feet_models.FootImage
    context_object_name = "foot_images"
    template_name = "feet/feet-cropper-left.html"

    def get(self, request, *args, **kwargs):
        try:
            foot = self.request.session["foot_images"]
        except KeyError:
            messages.error(self.request, _("問題が発生しました。もう一度試してみてください。"))
            return redirect(reverse("users:footsizes"))
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return feet_models.FootImage.objects.get(
                pk=self.request.session["foot_images"]
            )
        except KeyError:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = feet_forms.FootImageDataForm()
        return context

    def post(self, *args, **kwargs):
        # 画像情報をデータベースに反映する
        image_data = self.request.POST.get("image_data")
        processed_foot = feet_models.ProcessedFootImage.objects.create(
            foot_left=base64_file(image_data)
        )
        self.request.session["processed_foot"] = processed_foot.pk
        return redirect("users:crop-right")


class RightFootsizePerspeciveCropperView(mixins.LoggedInOnlyView, DetailView):

    """ 右足のイメージをクロップするためのツールを提供する """

    model = feet_models.FootImage
    context_object_name = "foot_images"
    template_name = "feet/feet-cropper-right.html"

    def get(self, request, *args, **kwargs):
        # セッションから足イメージの情報を取得してみる
        try:
            foot = self.request.session["foot_images"]
        # セッションに足イメージの情報が無かったらマイ足サイズ画面に戻る
        except KeyError:
            messages.error(self.request, _("問題が発生しました。もう一度試してみてください。"))
            return redirect(reverse("users:footsizes"))
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return feet_models.FootImage.objects.get(
                pk=self.request.session["foot_images"]
            )
        except KeyError:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = feet_forms.FootImageDataForm()
        return context

    def post(self, *args, **kwargs):
        processed_foot_pk = self.request.session["processed_foot"]
        # 画像情報をデータベースに反映する
        image_data = self.request.POST.get("image_data")
        processed_foot = feet_models.ProcessedFootImage.objects.get(
            pk=processed_foot_pk
        )
        processed_foot.foot_right = base64_file(image_data)
        processed_foot.save()
        return redirect("users:analyze", pk=processed_foot.pk)


@login_required()
def footsizes_analysis(request, *args, **kwargs):
    pk = kwargs.get("pk")
    instance = feet_models.ProcessedFootImage.objects.get(pk=pk)
    foot_left = instance.foot_left
    foot_right = instance.foot_right
    # イメージから足サイズを計算する
    length_left, width_left = analyze.analyze(foot_left)
    length_right, width_right = analyze.analyze(foot_right)
    # ユーザーに足サイズデータを登録・更新する
    if request.user.is_authenticated:
        user = request.user
    # 会員に既存の足サイズデータがある場合、データを更新する
    try:
        footsize = feet_models.Footsize.objects.get(user=user)
        footsize.length_left = length_left
        footsize.width_left = width_left
        footsize.length_right = length_right
        footsize.width_right = width_right
        footsize.save()
    # 会員に足サイズデータが存在しない場合、データを新規登録する
    except feet_models.Footsize.DoesNotExist:
        footsize = feet_models.Footsize.objects.create(
            user=user,
            length_left=length_left,
            length_right=length_right,
            width_left=width_left,
            width_right=width_right,
        )
    # カートに登録している他商品の足サイズと区分するためにセッションで足サイズを渡す
    request.session["length_left"] = int(length_left)
    request.session["length_right"] = int(length_right)
    request.session["width_left"] = int(width_left)
    request.session["width_right"] = int(width_right)
    # 前の画面から受け渡されたセッション値を削除する
    try:
        del request.session["foot_images"]
    except KeyError:
        messages.error(request, _("問題が発生しました。もう一度試してみてください。"))
        return redirect(reverse("users:footsizes"))
    try:
        del request.session["processed_foot"]
    except KeyError:
        messages.error(request, _("問題が発生しました。もう一度試してみてください。"))
        return redirect(reverse("users:footsizes"))
    messages.success(request, _("足サイズを登録しました。"))
    return redirect("users:footsizes")


class WithdrawalView(mixins.LoggedInOnlyView, FormView):

    """ 会員脱退ビュー """

    template_name = "users/withdrawal.html"
    form_class = forms.WithdrawalForm
    success_url = reverse_lazy("users:withdrawal-check")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        if self.request.user.email != email:
            messages.error(self.request, _("会員様のメールアドレスとは違います。"))
            return redirect(reverse("users:withdrawal"))
        else:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return super().form_valid(form)
            else:
                messages.error(self.request, _("パスワードをもう一度確認してください。"))
                return redirect(reverse("users:withdrawal"))


class WithdrawalCheckView(mixins.LoggedInOnlyView, DeleteView):

    """ 脱退処理前にもう一度確認してもらうためのビュー """

    model = models.User
    template_name = "users/withdrawal-check.html"

    def get(self, request):
        return render(request, self.template_name)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("users:withdrawal-done")


class WithdrawalDoneView(View):

    """ 会員脱退完了 """

    template_name = "users/withdrawal-done.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


def switch_language(request):

    """ 言語切り替えビュー """

    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
