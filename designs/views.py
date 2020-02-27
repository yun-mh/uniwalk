import base64, json
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View, ListView
from designs import models as design_models
from products import models as product_models
from users import models as user_models
from . import models, forms


# インコードした画像データを画像にデコードする関数
def base64_file(data, name=None):
    _format, _img_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name="{}.{}".format(name, ext))


class CustomizeView(ListView):

    """ デザインカスタマイズ """

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
        designs = (
            models.Design.objects.filter(product=pk).exclude(user__isnull=True).all()
        )
        return sorted(designs, key=lambda design: design.total_likes, reverse=True)

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        materials = design_models.Material.objects.all().order_by("created")
        context = super(CustomizeView, self).get_context_data(*args, **kwargs)
        for material in materials:
            context["mat" + str(material.pk)] = material
        context["product"] = product_models.Product.objects.get(pk=pk)
        context["template"] = product_models.Template.objects.get(product=pk)
        context["form"] = forms.CustomizeForm()
        return context

    def post(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        customize_form = forms.CustomizeForm(self.request.POST)
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None
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
            outsole_material_left=models.Material.objects.get(
                pk=customize_data["outsole_material_left"]
            ),
            midsole_material_left=models.Material.objects.get(
                pk=customize_data["midsole_material_left"]
            ),
            uppersole_material_left=models.Material.objects.get(
                pk=customize_data["uppersole_material_left"]
            ),
            shoelace_material_left=models.Material.objects.get(
                pk=customize_data["shoelace_material_left"]
            ),
            tongue_material_left=models.Material.objects.get(
                pk=customize_data["tongue_material_left"]
            ),
            outsole_material_right=models.Material.objects.get(
                pk=customize_data["outsole_material_right"]
            ),
            midsole_material_right=models.Material.objects.get(
                pk=customize_data["midsole_material_right"]
            ),
            uppersole_material_right=models.Material.objects.get(
                pk=customize_data["uppersole_material_right"]
            ),
            shoelace_material_right=models.Material.objects.get(
                pk=customize_data["shoelace_material_right"]
            ),
            tongue_material_right=models.Material.objects.get(
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
        self.request.session["product"] = pk
        self.request.session["design"] = new_design.pk
        return redirect("feet:check")


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
        name_outsole_material_left = models.Material.objects.get(
            pk=request.POST.get("outsole_material_left")
        ).name
        name_midsole_material_left = models.Material.objects.get(
            pk=request.POST.get("midsole_material_left")
        ).name
        name_uppersole_material_left = models.Material.objects.get(
            pk=request.POST.get("uppersole_material_left")
        ).name
        name_shoelace_material_left = models.Material.objects.get(
            pk=request.POST.get("shoelace_material_left")
        ).name
        name_tongue_material_left = models.Material.objects.get(
            pk=request.POST.get("tongue_material_left")
        ).name
        name_outsole_material_right = models.Material.objects.get(
            pk=request.POST.get("outsole_material_right")
        ).name
        name_midsole_material_right = models.Material.objects.get(
            pk=request.POST.get("midsole_material_right")
        ).name
        name_uppersole_material_right = models.Material.objects.get(
            pk=request.POST.get("uppersole_material_right")
        ).name
        name_shoelace_material_right = models.Material.objects.get(
            pk=request.POST.get("shoelace_material_right")
        ).name
        name_tongue_material_right = models.Material.objects.get(
            pk=request.POST.get("tongue_material_right")
        ).name
        outsole_material_left = models.Material.objects.get(
            pk=request.POST.get("outsole_material_left")
        ).file.url
        midsole_material_left = models.Material.objects.get(
            pk=request.POST.get("midsole_material_left")
        ).file.url
        uppersole_material_left = models.Material.objects.get(
            pk=request.POST.get("uppersole_material_left")
        ).file.url
        shoelace_material_left = models.Material.objects.get(
            pk=request.POST.get("shoelace_material_left")
        ).file.url
        tongue_material_left = models.Material.objects.get(
            pk=request.POST.get("tongue_material_left")
        ).file.url
        outsole_material_right = models.Material.objects.get(
            pk=request.POST.get("outsole_material_right")
        ).file.url
        midsole_material_right = models.Material.objects.get(
            pk=request.POST.get("midsole_material_right")
        ).file.url
        uppersole_material_right = models.Material.objects.get(
            pk=request.POST.get("uppersole_material_right")
        ).file.url
        shoelace_material_right = models.Material.objects.get(
            pk=request.POST.get("shoelace_material_right")
        ).file.url
        tongue_material_right = models.Material.objects.get(
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
                "name_outsole_material_left": name_outsole_material_left,
                "name_midsole_material_left": name_midsole_material_left,
                "name_uppersole_material_left": name_uppersole_material_left,
                "name_shoelace_material_left": name_shoelace_material_left,
                "name_tongue_material_left": name_tongue_material_left,
                "name_outsole_material_right": name_outsole_material_right,
                "name_midsole_material_right": name_midsole_material_right,
                "name_uppersole_material_right": name_uppersole_material_right,
                "name_shoelace_material_right": name_shoelace_material_right,
                "name_tongue_material_right": name_tongue_material_right,
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


class GalleriesListView(ListView):

    """ デザインギャラリー(全体) """

    model = models.Design
    paginate_by = 5
    context_object_name = "designs"
    extra_context = {
        "designs_all": models.Design.objects.all().exclude(user__isnull=True),
        "products": product_models.Product.objects.all(),
        "count": len(product_models.Product.objects.all()),
        "categories": product_models.Category.objects.all(),
    }
    template_name = "galleries/galleries_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        designs = models.Design.objects.filter(likes=self.request.user.pk)
        check_like = [design.pk for design in designs]
        context["check_like"] = check_like
        return context

    def get_queryset(self):
        designs = models.Design.objects.all().exclude(user__isnull=True)
        return sorted(designs, key=lambda design: design.total_likes, reverse=True)


class GalleriesListByCategoryView(ListView):

    """ デザインギャラリー(カテゴリー別) """

    model = models.Design
    paginate_by = 5
    context_object_name = "designs"
    extra_context = {
        "designs_all": models.Design.objects.all().exclude(user__isnull=True),
        "products": product_models.Product.objects.all(),
        "count": len(product_models.Product.objects.all()),
        "categories": product_models.Category.objects.all(),
    }
    template_name = "galleries/galleries_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        designs = models.Design.objects.filter(likes=self.request.user.pk)
        check_like = [design.pk for design in designs]
        context["check_like"] = check_like
        return context

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        designs = models.Design.objects.filter(product__category=pk).exclude(
            user__isnull=True
        )
        return sorted(designs, key=lambda design: design.total_likes, reverse=True)


class GalleriesListByProductView(ListView):

    """ デザインギャラリー(商品別) """

    model = models.Design
    paginate_by = 5
    context_object_name = "designs"
    extra_context = {
        "designs_all": models.Design.objects.all().exclude(user__isnull=True),
        "products": product_models.Product.objects.all(),
        "count": len(product_models.Product.objects.all()),
        "categories": product_models.Category.objects.all(),
    }
    template_name = "galleries/galleries_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        designs = models.Design.objects.filter(likes=self.request.user.pk)
        check_like = [design.pk for design in designs]
        context["check_like"] = check_like
        return context

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        designs = models.Design.objects.filter(product=pk).exclude(user__isnull=True)
        return sorted(designs, key=lambda design: design.total_likes, reverse=True)


# デザインに対した「いいね！」機能
def design_like(request):
    if request.method == "POST":
        user = request.user
        design_pk = request.POST.get("pk", None)
        design = models.Design.objects.get(pk=design_pk)

        if design.likes.filter(email=user.email).exists():
            design.likes.remove(user)
            check_like = False
        else:
            design.likes.add(user)
            check_like = True
        likes_count = str(design.total_likes)
        response = json.dumps(
            {"likes_count": likes_count, "check_like": str(check_like)}
        )
    return HttpResponse(response, content_type="application/json")

