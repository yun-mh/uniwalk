import base64, json
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView
from . import models, forms
from products import models as product_models
from designs import models as design_models


def base64_file(data, name=None):
    _format, _img_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name="{}.{}".format(name, ext))


class CustomizeView(ListView):

    model = models.Design
    template_name = "designs/design-customize.html"
    context_object_name = "designs"
    paginate_by = 5

    def get_template_names(self):
        if self.request.is_ajax():
            return ["mixins/designs/related_design_card.html"]
        return super(CustomizeView, self).get_template_names()

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return (
            models.Design.objects.filter(product=pk)
            .exclude(user__isnull=True)
            .order_by("-created")
        )

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        context = super(CustomizeView, self).get_context_data(*args, **kwargs)
        context["product"] = product_models.Product.objects.get(pk=pk)
        context["template"] = product_models.Template.objects.get(product=pk)
        context["materials"] = product_models.Material.objects.all()
        context["form"] = forms.CustomizeForm()
        return context

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
                # liner_color_left=customize_data["postal_code_recipient"],
                outsole_color_right=customize_data["outsole_color_right"],
                midsole_color_right=customize_data["midsole_color_right"],
                uppersole_color_right=customize_data["uppersole_color_right"],
                shoelace_color_right=customize_data["shoelace_color_right"],
                tongue_color_right=customize_data["tongue_color_right"],
                # liner_color_right=customize_data["address_detail_recipient"],
            )
        else:
            new_design = design_models.Design.objects.create(
                product=product_models.Product.objects.get(pk=pk),
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

        # 画像情報をデータベースに反映する
        image_data = self.request.POST.get("image_data")
        design_models.Image.objects.create(
            design=new_design, side_left=base64_file(image_data),
        )
        self.request.session["design"] = new_design.pk

        return redirect("feet:measure", pk=pk)


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
            }
        )
        return HttpResponse(response, content_type="application/json")
    else:
        raise Http404
