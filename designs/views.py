from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, View
from . import models, forms
from products import models as product_models
from designs import models as design_models


class CustomizeView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get("pk")
        product = product_models.Product.objects.all().get(pk=pk)
        template = product_models.Template.objects.get(product=pk)
        materials = product_models.Material.objects.all()
        customize_form = forms.CustomizeForm()
        return render(
            request,
            "designs/design-customize.html",
            {
                "product": product,
                "template": template,
                "materials": materials,
                "form": customize_form,
            },
        )

    def post(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        customize_form = forms.CustomizeForm(self.request.POST)
        customize_data = {
            "outsole_color_left": self.request.POST.get("outsole_color_left"),
            "midsole_color_left": self.request.POST.get("midsole_color_left"),
            "uppersole_color_left": self.request.POST.get("uppersole_color_left"),
            "shoelace_color_left": self.request.POST.get("shoelace_color_left"),
            "tongue_color_left": self.request.POST.get("tongue_color_left"),
            "liner_color_left": self.request.POST.get("liner_color_left"),
            "outsole_color_right": self.request.POST.get("outsole_color_right"),
            "midsole_color_right": self.request.POST.get("midsole_color_right"),
            "uppersole_color_right": self.request.POST.get("uppersole_color_right"),
            "shoelace_color_right": self.request.POST.get("shoelace_color_right"),
            "tongue_color_right": self.request.POST.get("tongue_color_right"),
            "liner_color_right": self.request.POST.get("liner_color_right"),
        }
        design_models.Design.objects.create(
            outsole_color_left=customize_data["outsole_color_left"],
            midsole_color_left=customize_data["midsole_color_left"],
            uppersole_color_left=customize_data["uppersole_color_left"],
            shoelace_color_left=customize_data["shoelace_color_left"],
            tongue_color_left=customize_data["tongue_color_left"],
            # liner_color_left=customize_data["postal_code_recipient"],
            outsole_color_right=customize_data["outsole_color_right"],
            midsole_color_right=customize_data["midsole_color_right"],
            uppersole_color_right=customize_data["uppersole_color_right"],
            shoelace_color_right=customize_data["shoelace_color_right"],
            tongue_color_right=customize_data["tongue_color_right"],
            # liner_color_right=customize_data["address_detail_recipient"],
        )
        return redirect('feet:measure', pk=pk)
