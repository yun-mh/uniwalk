from django.shortcuts import render
from django.views.generic import CreateView, View
from designs import models as design_models
from products import models as product_models
from . import models


class FootsizesMeasureView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get("pk")
        design_pk = request.session["design"]
        product = product_models.Product.objects.all().get(pk=pk)
        design = design_models.Design.objects.get(pk=design_pk)
        return render(
            request, "feet/feet-measure.html", {"product": product, "design": design}
        )

    # def post(self, request, *args, **kwargs):
    #     if "footsize_fill" in request.POST:
    #         member_form = user_forms.LoginForm(request.POST, prefix="member")
    #         if member_form.is_valid():
    #             member_email = member_form.cleaned_data.get("email")
    #             member_password = member_form.cleaned_data.get("password")
    #             user = authenticate(
    #                 request, email=member_email, password=member_password
    #             )
    #             if user is not None:
    #                 login(request, user)
    #                 return redirect(reverse("orders:checkout"))
    #         guest_form = forms.GuestForm(prefix="guest")

    #     elif "guest_login" in request.POST:
    #         guest_form = forms.GuestForm(request.POST, prefix="guest")
    #         if guest_form.is_valid():
    #             guest_email = guest_form.cleaned_data.get("email")
    #             try:
    #                 user_models.Guest.objects.get(email=guest_email)
    #             except user_models.Guest.DoesNotExist:
    #                 user_models.Guest.objects.create(email=guest_email)
    #             request.session["guest_email"] = guest_email
    #             return redirect(reverse("orders:checkout"))
    #         member_form = user_forms.LoginForm(prefix="member")
    # else:
    #     guest_form = forms.GuestForm(prefix="guest")
    #     member_form = user_forms.LoginForm(prefix="member")
    # context = {"member_form": member_form, "guest_form": guest_form}
    # return render(request, "orders/member-or-guest.html", context)
