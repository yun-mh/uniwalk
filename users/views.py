from django.shortcuts import render, reverse, redirect
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, FormView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)
from cards import models as card_models
from carts import models as cart_models
from orders import models as order_models
from designs import models as design_models
from designs import forms as design_forms
from feet import models as feet_models
from products import models as product_models
from . import forms, models, mixins
import stripe, base64, json


stripe.api_key = settings.STRIPE_SECRET_KEY

def base64_file(data, name=None):
    _format, _img_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    result = ContentFile(base64.b64decode(_img_str), name="{}.{}".format(name, ext))
    return result

class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            session_key = self.request.session.session_key
            cart_models.Cart.objects.filter(session_key=session_key).update(user_id=self.request.user.pk)
            messages.success(self.request, _(f"ログインしました。"))
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, _("ログアウトしました。"))
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

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
            _("UniWalk　会員登録ありがとうございます。"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        del request.session["data"]
        return redirect(reverse("users:signup-success"))


class SignupSuccessView(mixins.LoggedOutOnlyView, View):
    def get(self, request):
        return render(request, "users/signup-success.html")


class PasswordResetView(PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = "users/password-reset.html"
    subject_template_name = "emails/password-reset-subject.txt"
    email_template_name = "emails/password-reset-email.html"
    success_url = reverse_lazy("users:password-reset-done")


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password-reset-done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    template_name = "users/password-reset-confirm.html"
    success_url = reverse_lazy("users:password-reset-complete")

    def form_valid(self, form):
        email = self.user.email
        html_message = render_to_string("emails/password-reset-done.html")
        send_mail(
            _("パスワード再設定完了のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password-reset-complete.html"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
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
            _("UniWalk会員情報変更のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class PasswordChangeView(mixins.LoggedInOnlyView, PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = 'users/password-change.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        email = self.request.user.email
        html_message = render_to_string("emails/password-change-done.html")
        send_mail(
            _("UniWalkパスワード変更のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, _(f"パスワードを変更しました。"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("users:update-profile")


class OrdersListView(mixins.LoggedInOnlyView, ListView):
    model = order_models.Order
    template_name = "orders/order-list.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        try:
            return order_models.Order.objects.filter(user_id=self.request.user.pk).order_by("-order_date")
        except order_models.Order.DoesNotExist:
            return None

    def post(self, *args, **kwargs):
        order_pk = self.request.POST.get("target-order")
        target = order_models.Order.objects.filter(pk=order_pk)
        cancel = order_models.Step.objects.get(step_code="T99")
        target.update(
            step=cancel
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
        return order_models.Order.objects.filter(user_id=self.request.user.pk).get(pk=self.kwargs.get("order_pk"))

    def post(self, *args, **kwargs):
        order_pk = self.request.POST.get("target-order")
        target = order_models.Order.objects.filter(pk=order_pk)
        cancel = order_models.Step.objects.get(step_code="T99")
        target.update(
            step=cancel
        )
        messages.success(self.request, _("注文を取消しました。"))
        return redirect("users:orders")


class CardsListView(mixins.LoggedInOnlyView, FormView):
    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            cards = stripe.Customer.list_sources(
                        user.stripe_customer_id,
                        object='card'
                    )
        except:
            cards = {"data": []}
        card_list = cards["data"]
        context = {}
        if len(card_list) > 0:
            context = {
                "cards": card_list,
            }
        return render(self.request, "cards/card-list.html", context)

    def post(self, *args, **kwargs):
        card_customer = self.request.POST.get("target-customer")
        card_id = self.request.POST.get("target-card")
        card_fingerprint = self.request.POST.get("target-fingerprint")
        stripe.Customer.delete_source(
            card_customer,
            card_id,
        )
        target = card_models.Card.objects.get(
            stripe_customer_id=card_customer,
            fingerprint=card_fingerprint,
        )
        target.delete()
        messages.success(self.request, _("カードを登録解除しました。"))
        return redirect("users:cards")


class CardsAddView(mixins.LoggedInOnlyView, View):
    def get(self, *args, **kwargs):
        # user = self.request.user
        add_card_form = forms.AddCardForm()
        context = {
            "add_card_form": add_card_form
        }
        return render(self.request, "cards/card-registration.html", context)

    def post(self, *args, **kwargs):
        add_card_form = forms.AddCardForm(self.request.POST)
        if add_card_form.is_valid():
            user = models.User.objects.get(email=self.request.user)
            token = add_card_form.cleaned_data.get("stripeToken")
            if user.stripe_customer_id != '' and user.stripe_customer_id is not None:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
                card_id = stripe.Token.retrieve(token).card.id
                current_fingerprint = stripe.Token.retrieve(token).card.fingerprint
                current_exp_month = stripe.Token.retrieve(token).card.exp_month
                current_exp_year = stripe.Token.retrieve(token).card.exp_year
                try:
                    card_models.Card.objects.get(
                        fingerprint=current_fingerprint,
                        exp_month=current_exp_month,
                        exp_year=current_exp_year,
                    )
                except card_models.Card.DoesNotExist:
                    customer.sources.create(card=token)
                    card_models.Card.objects.create(
                        stripe_customer_id=user.stripe_customer_id,
                        card_id=card_id,
                        fingerprint=current_fingerprint,
                        exp_month=current_exp_month,
                        exp_year=current_exp_year,
                    )
            else:
                card_id = stripe.Token.retrieve(token).card.id
                current_fingerprint = stripe.Token.retrieve(token).card.fingerprint
                current_exp_month = stripe.Token.retrieve(token).card.exp_month
                current_exp_year = stripe.Token.retrieve(token).card.exp_year
                customer = stripe.Customer.create(
                    email=self.request.user.email,
                )
                user.stripe_customer_id = customer['id']
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
    model = design_models.Design
    template_name = "designs/design-list.html"
    context_object_name = "designs"
    paginate_by = 5

    def get_queryset(self):
        try:
            return design_models.Design.objects.filter(user_id=self.request.user.pk).order_by("-created")
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

    model = product_models.Product
    template_name = "designs/select-products.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        return product_models.Product.objects.all().order_by("-created")


class MemberCustomizeView(mixins.LoggedInOnlyView, ListView):

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
        designs = design_models.Design.objects.filter(product=pk).exclude(user__isnull=True).all()
        return sorted(designs, key= lambda design: design.total_likes, reverse=True)

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        materials = design_models.Material.objects.all().order_by("created")
        context = super(MemberCustomizeView, self).get_context_data(*args, **kwargs)
        for material in materials:
            context["mat" + str(material.pk) ] = material
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
            "uppersole_material_right": self.request.POST.get("uppersole_material_right"),
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
                outsole_material_left=design_models.Material.objects.get(pk=customize_data["outsole_material_left"]),
                midsole_material_left=design_models.Material.objects.get(pk=customize_data["midsole_material_left"]),
                uppersole_material_left=design_models.Material.objects.get(pk=customize_data["uppersole_material_left"]),
                shoelace_material_left=design_models.Material.objects.get(pk=customize_data["shoelace_material_left"]),
                tongue_material_left=design_models.Material.objects.get(pk=customize_data["tongue_material_left"]),
                outsole_material_right=design_models.Material.objects.get(pk=customize_data["outsole_material_right"]),
                midsole_material_right=design_models.Material.objects.get(pk=customize_data["midsole_material_right"]),
                uppersole_material_right=design_models.Material.objects.get(pk=customize_data["uppersole_material_right"]),
                shoelace_material_right=design_models.Material.objects.get(pk=customize_data["shoelace_material_right"]),
                tongue_material_right=design_models.Material.objects.get(pk=customize_data["tongue_material_right"]),
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
                outsole_material_left=design_models.Material.objects.get(pk=customize_data["outsole_material_left"]),
                midsole_material_left=design_models.Material.objects.get(pk=customize_data["midsole_material_left"]),
                uppersole_material_left=design_models.Material.objects.get(pk=customize_data["uppersole_material_left"]),
                shoelace_material_left=design_models.Material.objects.get(pk=customize_data["shoelace_material_left"]),
                tongue_material_left=design_models.Material.objects.get(pk=customize_data["tongue_material_left"]),
                outsole_material_right=design_models.Material.objects.get(pk=customize_data["outsole_material_right"]),
                midsole_material_right=design_models.Material.objects.get(pk=customize_data["midsole_material_right"]),
                uppersole_material_right=design_models.Material.objects.get(pk=customize_data["uppersole_material_right"]),
                shoelace_material_right=design_models.Material.objects.get(pk=customize_data["shoelace_material_right"]),
                tongue_material_right=design_models.Material.objects.get(pk=customize_data["tongue_material_right"]),
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
        outsole_material_left = design_models.Material.objects.get(pk=request.POST.get("outsole_material_left")).file.url
        midsole_material_left = design_models.Material.objects.get(pk=request.POST.get("midsole_material_left")).file.url
        uppersole_material_left = design_models.Material.objects.get(pk=request.POST.get("uppersole_material_left")).file.url
        shoelace_material_left = design_models.Material.objects.get(pk=request.POST.get("shoelace_material_left")).file.url
        tongue_material_left = design_models.Material.objects.get(pk=request.POST.get("tongue_material_left")).file.url
        outsole_material_right = design_models.Material.objects.get(pk=request.POST.get("outsole_material_right")).file.url
        midsole_material_right = design_models.Material.objects.get(pk=request.POST.get("midsole_material_right")).file.url
        uppersole_material_right = design_models.Material.objects.get(pk=request.POST.get("uppersole_material_right")).file.url
        shoelace_material_right = design_models.Material.objects.get(pk=request.POST.get("shoelace_material_right")).file.url
        tongue_material_right = design_models.Material.objects.get(pk=request.POST.get("tongue_material_right")).file.url
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
        designs = design_models.Design.objects.filter(product=pk).exclude(user__isnull=True).all()
        return sorted(designs, key= lambda design: design.total_likes, reverse=True)

    def get_context_data(self, *args, **kwargs):
        pk = self.request.session["product"]
        design_pk = self.request.session["design"]
        materials = design_models.Material.objects.all().order_by("created")
        design_before = design_models.Design.objects.get(pk=design_pk)
        context = super(MemberCustomizeModifyView, self).get_context_data(*args, **kwargs)
        for material in materials:
            context["mat" + str(material.pk) ] = material
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
            "uppersole_material_right": self.request.POST.get("uppersole_material_right"),
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
                outsole_material_left=design_models.Material.objects.get(pk=customize_data["outsole_material_left"]),
                midsole_material_left=design_models.Material.objects.get(pk=customize_data["midsole_material_left"]),
                uppersole_material_left=design_models.Material.objects.get(pk=customize_data["uppersole_material_left"]),
                shoelace_material_left=design_models.Material.objects.get(pk=customize_data["shoelace_material_left"]),
                tongue_material_left=design_models.Material.objects.get(pk=customize_data["tongue_material_left"]),
                outsole_material_right=design_models.Material.objects.get(pk=customize_data["outsole_material_right"]),
                midsole_material_right=design_models.Material.objects.get(pk=customize_data["midsole_material_right"]),
                uppersole_material_right=design_models.Material.objects.get(pk=customize_data["uppersole_material_right"]),
                shoelace_material_right=design_models.Material.objects.get(pk=customize_data["shoelace_material_right"]),
                tongue_material_right=design_models.Material.objects.get(pk=customize_data["tongue_material_right"]),
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
                outsole_material_left=design_models.Material.objects.get(pk=customize_data["outsole_material_left"]),
                midsole_material_left=design_models.Material.objects.get(pk=customize_data["midsole_material_left"]),
                uppersole_material_left=design_models.Material.objects.get(pk=customize_data["uppersole_material_left"]),
                shoelace_material_left=design_models.Material.objects.get(pk=customize_data["shoelace_material_left"]),
                tongue_material_left=design_models.Material.objects.get(pk=customize_data["tongue_material_left"]),
                outsole_material_right=design_models.Material.objects.get(pk=customize_data["outsole_material_right"]),
                midsole_material_right=design_models.Material.objects.get(pk=customize_data["midsole_material_right"]),
                uppersole_material_right=design_models.Material.objects.get(pk=customize_data["uppersole_material_right"]),
                shoelace_material_right=design_models.Material.objects.get(pk=customize_data["shoelace_material_right"]),
                tongue_material_right=design_models.Material.objects.get(pk=customize_data["tongue_material_right"]),
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
    model = feet_models.Footsize
    template_name = "feet/feet-list.html"
    context_object_name = "feet"

    def get_queryset(self):
        try:
            return feet_models.Footsize.objects.get(user_id=self.request.user.pk)
        except feet_models.Footsize.DoesNotExist:
            return None


class WithdrawalView(mixins.LoggedInOnlyView, FormView):
    template_name = "users/withdrawal.html"
    form_class = forms.WithdrawalForm
    success_url = reverse_lazy("users:withdrawal-check")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if self.request.user.email != email:
            messages.error(self.request, _("会員様のメールアドレスと入力したメールアドレスが違います。"))
            return redirect(reverse("users:withdrawal"))
        return super().form_valid(form)


class WithdrawalCheckView(mixins.LoggedInOnlyView, DeleteView):
    model = models.User
    template_name = "users/withdrawal-check.html"

    def get(self, request):
        return render(request, self.template_name)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("users:withdrawal-done")


class WithdrawalDoneView(View):
    template_name = "users/withdrawal-done.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
