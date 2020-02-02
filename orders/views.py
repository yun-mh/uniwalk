from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, render_to_response
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, FormView, DetailView
from users import mixins
from users import forms as user_forms
from users import models as user_models
from designs import models as design_models
from cards import models as card_models
from carts import models as cart_models
from . import forms, models
from localflavor.jp.jp_prefectures import JP_PREFECTURE_CODES, JP_PREFECTURES
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def member_or_guest_login(request):
    
    """ 会員・ゲスト確認ビュー """
    
    if request.user.is_authenticated:
        return redirect("orders:checkout")
    if request.method == "POST":
        if "member_login" in request.POST:
            member_form = user_forms.LoginForm(request.POST, prefix="member")
            if member_form.is_valid():
                member_email = member_form.cleaned_data.get("email")
                member_password = member_form.cleaned_data.get("password")
                user = authenticate(
                    request, email=member_email, password=member_password
                )
                if user is not None:
                    login(request, user)
                    return redirect(reverse("orders:checkout"))
            guest_form = forms.GuestForm(prefix="guest")
        elif "guest_login" in request.POST:
            guest_form = forms.GuestForm(request.POST, prefix="guest")
            if guest_form.is_valid():
                guest_email = guest_form.cleaned_data.get("email")
                try:
                    user_models.Guest.objects.get(email=guest_email)
                except user_models.Guest.DoesNotExist:
                    user_models.Guest.objects.create(email=guest_email)
                request.session["guest_email"] = guest_email
                return redirect(reverse("orders:checkout"))
            member_form = user_forms.LoginForm(prefix="member")
    else:
        guest_form = forms.GuestForm(prefix="guest")
        member_form = user_forms.LoginForm(prefix="member")
    context = {"member_form": member_form, "guest_form": guest_form}
    return render(request, "orders/member-or-guest.html", context)


class CheckoutView(FormView):

    """ 注文情報入力 """

    def get(self, *args, **kwargs):
        recipient_form = forms.CheckoutForm()
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_form": recipient_form,
            "cart": cart,
            "total": total,
        }
        if self.request.user.is_authenticated:
            recipient = user_models.User.objects.get(email=self.request.user).as_dict()
            context["recipient_info"] = recipient

        return render(self.request, "orders/checkout.html", context)

    def post(self, *args, **kwargs):
        recipient_form = forms.CheckoutForm(self.request.POST)
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_form": recipient_form,
            "cart": cart,
            "total": total,
        }
        if recipient_form.is_valid():
            recipient_data = {
                "last_name_recipient": recipient_form.cleaned_data.get(
                    "last_name_recipient"
                ),
                "first_name_recipient": recipient_form.cleaned_data.get(
                    "first_name_recipient"
                ),
                "last_name_recipient_kana": recipient_form.cleaned_data.get(
                    "last_name_recipient_kana"
                ),
                "first_name_recipient_kana": recipient_form.cleaned_data.get(
                    "first_name_recipient_kana"
                ),
                "phone_number_recipient": recipient_form.cleaned_data.get(
                    "phone_number_recipient"
                ),
                "postal_code_recipient": recipient_form.cleaned_data.get(
                    "postal_code_recipient"
                ),
                "prefecture_recipient": recipient_form.cleaned_data.get(
                    "prefecture_recipient"
                ),
                "address_city_recipient": recipient_form.cleaned_data.get(
                    "address_city_recipient"
                ),
                "address_detail_recipient": recipient_form.cleaned_data.get(
                    "address_detail_recipient"
                ),
            }
            self.request.session["recipient_data"] = recipient_data
            return redirect(reverse("orders:select-payment"))
        return render(self.request, "orders/checkout.html", context)


class SelectPaymentView(FormView):

    """ 決済手段入力 """

    def get(self, *args, **kwargs):
        orderer_form = forms.SelectPaymentForm()
        recipient_data = self.request.session["recipient_data"]
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_data": recipient_data,
            "recipient_pref": JP_PREFECTURE_CODES[int(recipient_data["prefecture_recipient"]) - 1][1],
            "orderer_form": orderer_form,
            "cart": cart,
            "total": total,
        }
        return render(self.request, "orders/select-payment.html", context)

    def post(self, *args, **kwargs):
        orderer_form = forms.SelectPaymentForm(self.request.POST)
        recipient_data = self.request.session["recipient_data"]
        if orderer_form.is_valid():
            if orderer_form.cleaned_data.get("is_same_with_recipient") == True:
                orderer_data = {
                    "is_same_with_recipient": orderer_form.cleaned_data.get(
                        "is_same_with_recipient"
                    ),
                    "payment": orderer_form.cleaned_data.get("payment"),
                    "last_name_orderer": recipient_data["last_name_recipient"],
                    "first_name_orderer": recipient_data["first_name_recipient"],
                    "last_name_orderer_kana": recipient_data["last_name_recipient_kana"],
                    "first_name_orderer_kana": recipient_data["first_name_recipient_kana"],
                    "phone_number_orderer": recipient_data["phone_number_recipient"],
                    "postal_code_orderer": recipient_data["postal_code_recipient"],
                    "prefecture_orderer": recipient_data["prefecture_recipient"],
                    "address_city_orderer": recipient_data["address_city_recipient"],
                    "address_detail_orderer": recipient_data["address_detail_recipient"],
                }
            else:
                orderer_data = {
                    "is_same_with_recipient": orderer_form.cleaned_data.get(
                        "is_same_with_recipient"
                    ),
                    "payment": orderer_form.cleaned_data.get("payment"),
                    "last_name_orderer": orderer_form.cleaned_data.get("last_name_orderer"),
                    "first_name_orderer": orderer_form.cleaned_data.get(
                        "first_name_orderer"
                    ),
                    "last_name_orderer_kana": orderer_form.cleaned_data.get(
                        "last_name_orderer_kana"
                    ),
                    "first_name_orderer_kana": orderer_form.cleaned_data.get(
                        "first_name_orderer_kana"
                    ),
                    "phone_number_orderer": orderer_form.cleaned_data.get(
                        "phone_number_orderer"
                    ),
                    "postal_code_orderer": orderer_form.cleaned_data.get(
                        "postal_code_orderer"
                    ),
                    "prefecture_orderer": orderer_form.cleaned_data.get(
                        "prefecture_orderer"
                    ),
                    "address_city_orderer": orderer_form.cleaned_data.get(
                        "address_city_orderer"
                    ),
                    "address_detail_orderer": orderer_form.cleaned_data.get(
                        "address_detail_orderer"
                    ),
                }
            self.request.session["orderer_data"] = orderer_data
            return redirect(reverse("orders:order-check"))


class OrderCheckView(FormView):

    """ 注文情報確認及びカード情報入力(カード決済時) """

    def get(self, *args, **kwargs):
        card_form = forms.CardForm()
        recipient_data = self.request.session["recipient_data"]
        orderer_data = self.request.session["orderer_data"]
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        if self.request.user.is_authenticated:
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
                cards = card_list,
        else:
            cards = {"data": []}
            card_list = cards["data"]
        context = {
            "recipient_data": recipient_data,
            "recipient_pref": JP_PREFECTURE_CODES[int(recipient_data["prefecture_recipient"]) - 1][1],
            "orderer_data": orderer_data,
            "orderer_pref": JP_PREFECTURE_CODES[int(orderer_data["prefecture_orderer"]) - 1][1],
            "card_form": card_form,
            "cart": cart,
            "total": total,
            "cards": card_list,
        }
        return render(self.request, "orders/order-check.html", context)

    def post(self, *args, **kwargs):
        card_form = forms.CardForm(self.request.POST)
        recipient_data = self.request.session["recipient_data"]
        orderer_data = self.request.session["orderer_data"]
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity

        if card_form.is_valid():
            payment = orderer_data["payment"]
            token = card_form.cleaned_data.get("stripeToken")
            save = card_form.cleaned_data.get("save")
            use_default = card_form.cleaned_data.get("use_default")

            if payment == "P1":
                if self.request.user.is_authenticated:
                    user = user_models.User.objects.get(email=self.request.user)
                if save:
                    if user.stripe_customer_id != '' and user.stripe_customer_id is not None:
                        customer = stripe.Customer.retrieve(user.stripe_customer_id)
                        card_id = stripe.Token.retrieve(token).card.id
                        current_fingerprint = stripe.Token.retrieve(token).card.fingerprint
                        current_exp_month = stripe.Token.retrieve(token).card.exp_month
                        current_exp_year = stripe.Token.retrieve(token).card.exp_year
                        try:
                            used = card_models.Card.objects.get(
                                fingerprint=current_fingerprint,
                                exp_month=current_exp_month,
                                exp_year=current_exp_year,
                            )
                            try:
                                source = customer.retrieve_source(
                                    user.stripe_customer_id,
                                    used.card_id,
                                )
                            except:
                                pass
                        except card_models.Card.DoesNotExist:
                            source = customer.create_source(
                                user.stripe_customer_id,
                                source=token
                            )
                            card_models.Card.objects.create(
                                stripe_customer_id=user.stripe_customer_id,
                                card_id=card_id,
                                fingerprint=current_fingerprint,
                                exp_month=current_exp_month,
                                exp_year=current_exp_year,
                            )
                    else:
                        current_fingerprint = stripe.Token.retrieve(token).card.fingerprint
                        current_exp_month = stripe.Token.retrieve(token).card.exp_month
                        current_exp_year = stripe.Token.retrieve(token).card.exp_year
                        customer = stripe.Customer.create(
                            email=self.request.user.email,
                            name=orderer_data["first_name_orderer"] + " " + orderer_data["last_name_orderer"],
                        )
                        user.stripe_customer_id = customer['id']
                        user.save()
                        customer.sources.create(card=token) #???　保存しなくてもいいかも
                        card_models.Card.objects.create(
                            stripe_customer_id=user.stripe_customer_id,
                            fingerprint=current_fingerprint,
                            exp_month=current_exp_month,
                            exp_year=current_exp_year,
                        )
                try:
                    if save:
                        charge = stripe.Charge.create(
                            amount=total,
                            currency="JPY",
                            customer=user.stripe_customer_id,
                            source=source
                        )
                    elif use_default:
                        source = self.request.POST.get("use_default_card")
                        charge = stripe.Charge.create(
                            amount=total,
                            currency="JPY",
                            customer=user.stripe_customer_id,
                            source=source
                        )
                    else:
                        charge = stripe.Charge.create(
                            amount=total,
                            currency="JPY",
                            source=token
                        )
                    stripe_charge_id = charge["id"]

                except stripe.error.CardError as e:
                    body = e.json_body
                    err = body.get('error', {})
                    messages.warning(self.request, f"{err.get('message')}")
                    return redirect("/")

                except stripe.error.RateLimitError as e:
                    # Too many requests made to the API too quickly
                    messages.warning(self.request, "Rate limit error")
                    return redirect("/")

                except stripe.error.InvalidRequestError as e:
                    # Invalid parameters were supplied to Stripe's API
                    print(e)
                    messages.warning(self.request, "Invalid parameters")
                    # return redirect("orders:select-payment")

                except stripe.error.AuthenticationError as e:
                    # Authentication with Stripe's API failed
                    # (maybe you changed API keys recently)
                    messages.warning(self.request, "Not authenticated")
                    return redirect("/")

                except stripe.error.APIConnectionError as e:
                    # Network communication with Stripe failed
                    messages.warning(self.request, "Network error")
                    return redirect("/")

                except stripe.error.StripeError as e:
                    # Display a very generic error to the user, and maybe send
                    # yourself an email
                    messages.warning(
                        self.request, "Something went wrong. You were not charged. Please try again.")
                    return redirect("/")

                except Exception as e:
                    # send an email to ourselves
                    messages.warning(
                        self.request, "A serious error occurred. We have been notifed.")
                    return redirect("/")
            else:
                stripe_charge_id = None

            if self.request.user.is_authenticated:
                user = self.request.user
                guest = None
            else:
                user = None
                guest = user_models.Guest.objects.get(
                    email=self.request.session["guest_email"]
                )
            if payment == "P1":
                step = models.Step.objects.get(step_code="T02")
            else:
                step = models.Step.objects.get(step_code="T01")
            new_order = models.Order.objects.create(
                user=user,
                guest=guest,
                last_name_recipient=recipient_data["last_name_recipient"],
                first_name_recipient=recipient_data["first_name_recipient"],
                last_name_recipient_kana=recipient_data["last_name_recipient_kana"],
                first_name_recipient_kana=recipient_data["first_name_recipient_kana"],
                phone_number_recipient=recipient_data["phone_number_recipient"],
                postal_code_recipient=recipient_data["postal_code_recipient"],
                prefecture_recipient=recipient_data["prefecture_recipient"],
                address_city_recipient=recipient_data["address_city_recipient"],
                address_detail_recipient=recipient_data["address_detail_recipient"],
                last_name_orderer=orderer_data["last_name_orderer"],
                first_name_orderer=orderer_data["first_name_orderer"],
                last_name_orderer_kana=orderer_data["last_name_orderer_kana"],
                first_name_orderer_kana=orderer_data["first_name_orderer_kana"],
                phone_number_orderer=orderer_data["phone_number_orderer"],
                postal_code_orderer=orderer_data["postal_code_orderer"],
                prefecture_orderer=orderer_data["prefecture_orderer"],
                address_city_orderer=orderer_data["address_city_orderer"],
                address_detail_orderer=orderer_data["address_detail_orderer"],
                payment=orderer_data["payment"],
                step=step,
                amount=total,
                stripe_charge_id=stripe_charge_id,
            )
            for cart_item in cart_items:
                models.OrderItem.objects.create(
                    order=new_order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    front=design_models.Image.objects.get(design=cart_item.design.pk).front,
                    side=design_models.Image.objects.get(design=cart_item.design.pk).side,
                    up=design_models.Image.objects.get(design=cart_item.design.pk).up,
                    down=design_models.Image.objects.get(design=cart_item.design.pk).down,
                    outsole_color_left=design_models.Design.objects.get(pk=cart_item.design.pk).outsole_color_left,
                    outsole_material_left=design_models.Design.objects.get(pk=cart_item.design.pk).outsole_material_left,
                    midsole_color_left=design_models.Design.objects.get(pk=cart_item.design.pk).midsole_color_left,
                    midsole_material_left=design_models.Design.objects.get(pk=cart_item.design.pk).midsole_material_left,
                    uppersole_color_left=design_models.Design.objects.get(pk=cart_item.design.pk).uppersole_color_left,
                    uppersole_material_left=design_models.Design.objects.get(pk=cart_item.design.pk).uppersole_material_left,
                    shoelace_color_left=design_models.Design.objects.get(pk=cart_item.design.pk).shoelace_color_left,
                    shoelace_material_left=design_models.Design.objects.get(pk=cart_item.design.pk).shoelace_material_left,
                    tongue_color_left=design_models.Design.objects.get(pk=cart_item.design.pk).tongue_color_left,
                    tongue_material_left=design_models.Design.objects.get(pk=cart_item.design.pk).tongue_material_left,
                    outsole_color_right=design_models.Design.objects.get(pk=cart_item.design.pk).outsole_color_right,
                    outsole_material_right=design_models.Design.objects.get(pk=cart_item.design.pk).outsole_material_right,
                    midsole_color_right=design_models.Design.objects.get(pk=cart_item.design.pk).midsole_color_right,
                    midsole_material_right=design_models.Design.objects.get(pk=cart_item.design.pk).midsole_material_right,
                    uppersole_color_right=design_models.Design.objects.get(pk=cart_item.design.pk).uppersole_color_right,
                    uppersole_material_right=design_models.Design.objects.get(pk=cart_item.design.pk).uppersole_material_right,
                    shoelace_color_right=design_models.Design.objects.get(pk=cart_item.design.pk).shoelace_color_right,
                    shoelace_material_right=design_models.Design.objects.get(pk=cart_item.design.pk).shoelace_material_right,
                    tongue_color_right=design_models.Design.objects.get(pk=cart_item.design.pk).tongue_color_right,
                    tongue_material_right=design_models.Design.objects.get(pk=cart_item.design.pk).tongue_material_right,
                    customize_code=design_models.Design.objects.get(pk=cart_item.design.pk).customize_code,
                )
            try:
                email = self.request.user.email
            except:
                email = self.request.session["guest_email"]
            order_code = new_order.order_code
            cart_items.update(active=False)
            self.request.session.cycle_key_after_purchase()
            html_message = render_to_string("emails/purchase-done.html", {"order_code": order_code})
            send_mail(
                _("UniWalk　ご注文ありがとうございます。"),
                strip_tags(html_message),
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_message,
            )
            try:
                del self.request.session["guest_email"]
                del self.request.session["recipient_data"]
                del self.request.session["orderer_data"]
            except:
                pass
            return redirect("orders:checkout-done", order_code)


class CheckoutDoneView(View):

    """ 注文完了 """

    def get(self, request, *args, **kwargs):
        context = {
            "order_code": kwargs.get("order_code")
        }
        return render(request, "orders/checkout-done.html", context)


class OrderSearchView(FormView):

    """ 注文検索 """

    model = models.Order
    form_class = forms.OrderSearchForm
    template_name = "orders/order-search.html"
    success_url = reverse_lazy("orders:detail")

    def form_valid(self, form):
        order_code = form.cleaned_data.get("order_code")
        email = form.cleaned_data.get("email")
        try:
            order = models.Order.objects.get(order_code=order_code)
        except models.Order.DoesNotExist:
            messages.error(self.request, _("入力した情報をもう一度確認してください。"))
            return redirect("orders:search")
        try:
            if str(order.user) == email or str(order.guest.email) == email:
                return redirect("orders:detail", order_code)
        except AttributeError:
            messages.error(self.request, _("入力した情報をもう一度確認してください。"))
            return redirect("orders:search")


class OrderDetailView(DetailView):

    """ 注文詳細(注文番号で照会) """

    template_name = "orders/search-order-detail.html"
    context_object_name = "order"
    slug_field = 'order_code'
    slug_url_kwarg = 'order_code'

    def get_queryset(self):
        order_code = self.kwargs.get("order_code")
        try:
            return models.Order.objects.filter(order_code=order_code)
        except models.Order.DoesNotExist:
            return None
    
    def post(self, *args, **kwargs):
        order_code = self.kwargs.get("order_code")
        order_pk = self.request.POST.get("target-order")
        target = models.Order.objects.filter(pk=order_pk)
        cancel = models.Step.objects.get(step_code="T99")
        target.update(
            step=cancel
        )
        messages.success(self.request, _("注文を取消しました。"))
        return redirect("orders:detail", order_code)


class BillView(DetailView):

    """ 請求書発行 """

    template_name = "orders/bill.html"
    context_object_name = "order"
    slug_field = 'order_code'
    slug_url_kwarg = 'order_code'

    def get_queryset(self):
        order_code = self.kwargs.get("order_code")
        try:
            return models.Order.objects.filter(order_code=order_code)
        except models.Order.DoesNotExist:
            return None


class ReceiptView(DetailView):

    """ 領収書発行 """

    template_name = "orders/receipt.html"
    context_object_name = "order"
    slug_field = 'order_code'
    slug_url_kwarg = 'order_code'

    def get_queryset(self):
        order_code = self.kwargs.get("order_code")
        try:
            return models.Order.objects.filter(order_code=order_code)
        except models.Order.DoesNotExist:
            return None