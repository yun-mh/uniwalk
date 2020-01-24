from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from designs import models as design_models
from products import models as product_models
from . import models, forms


def footsizes_measure(request, *args, **kwargs):
    pk = kwargs.get("pk")
    design_pk = request.session["design"]
    if request.method == "POST":
        try:
            user = request.user
        except:
            user = None
        if "footsize-fill" in request.POST:
            footsize_fill_form = forms.FootsizeFillForm(request.POST, prefix="fill")
            if footsize_fill_form.is_valid():
                length_left = footsize_fill_form.cleaned_data.get("length_left")
                length_right = footsize_fill_form.cleaned_data.get("length_right")
                width_left = footsize_fill_form.cleaned_data.get("width_left")
                width_right = footsize_fill_form.cleaned_data.get("width_right")
                new_footsize = models.Footsize.objects.create(
                    user=user,
                    length_left=length_left,
                    length_right=length_right,
                    width_left=width_left,
                    width_right=width_right,
                )
                print(new_footsize)
                return redirect("carts:cart")
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
    else:
        footsize_fill_form = forms.FootsizeFillForm(prefix="fill")
        # member_form = user_forms.LoginForm(prefix="member")
    context = {"footsize_fill_form": footsize_fill_form}
    return render(request, "feet/feet-measure.html", context)
