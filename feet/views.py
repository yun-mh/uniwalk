from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from designs import models as design_models
from products import models as product_models
from . import models, forms, analyze
import base64


# インコードした画像データを画像にデコードする関数
def base64_file(data, name=None):
    _format, _img_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    result = ContentFile(base64.b64decode(_img_str), name="{}.{}".format(name, ext))
    return result


def have_footsize(request, *arg, **kwargs):

    """ 足サイズデータを既に持っているかどうかチェックする """

    if request.user.is_authenticated:
        user = request.user
        try:
            footsize = models.Footsize.objects.get(user=user)
            request.session["length_left"] = int(footsize.length_left)
            request.session["length_right"] = int(footsize.length_right)
            request.session["width_left"] = int(footsize.width_left)
            request.session["width_right"] = int(footsize.width_right)
            return render(request, "feet/feet-check.html")
        except models.Footsize.DoesNotExist:
            return redirect("feet:measure")
    return redirect("feet:measure")


def footsizes_measure(request, *args, **kwargs):

    """ 足サイズ測定 """

    # 次のページに渡すテータを取得するための操作
    pk = request.session["product"]
    design_pk = request.session["design"]

    # 足測定の結果をデータベースに反映する
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        # 記入式で足サイズを指定した場合
        if "footsize-fill" in request.POST:
            footsize_fill_form = forms.FootsizeFillForm(request.POST, prefix="fill")
            if footsize_fill_form.is_valid():
                length_left = footsize_fill_form.cleaned_data.get("length_left")
                width_left = footsize_fill_form.cleaned_data.get("width_left")
                length_right = footsize_fill_form.cleaned_data.get("length_right")
                width_right = footsize_fill_form.cleaned_data.get("width_right")
                # 会員に既存の足サイズデータがある場合、データを更新する
                try:
                    footsize = models.Footsize.objects.get(user=user)
                    footsize.length_left = length_left
                    footsize.length_right = length_right
                    footsize.width_left = width_left
                    footsize.width_right = width_right
                    footsize.save()
                # 会員に足サイズデータが存在しない場合、データを新規登録する
                except models.Footsize.DoesNotExist:
                    footsize = models.Footsize.objects.create(
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
                return redirect("carts:add_cart", pk=pk, design_pk=design_pk)
            else:
                messages.error(request, _("入力した情報をもう一度確認してください。"))
            footsize_image_form = forms.FootsizeImageForm(prefix="image")
        elif "footsize-image" in request.POST:
            footsize_image_form = forms.FootsizeImageForm(
                request.POST, request.FILES, prefix="image"
            )
            if footsize_image_form.is_valid():
                foot_images = models.FootImage(
                    foot_left=request.FILES["image-foot_left"],
                    foot_right=request.FILES["image-foot_right"],
                )
                foot_images.save()
                return redirect("feet:rotation", pk=foot_images.pk)
            footsize_fill_form = forms.FootsizeFillForm(prefix="fill")
    else:
        footsize_fill_form = forms.FootsizeFillForm(prefix="fill")
        footsize_image_form = forms.FootsizeImageForm(prefix="image")
    context = {
        "footsize_fill_form": footsize_fill_form,
        "footsize_image_form": footsize_image_form,
    }
    return render(request, "feet/feet-measure.html", context)


class FootImageRotationView(DetailView):

    """ 足イメージをローテートするためのツールを提供する """

    model = models.FootImage
    context_object_name = "foot_images"
    template_name = "feet/feet-rotation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.FootImageRotationForm()
        return context

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        feet = models.FootImage.objects.get(pk=pk)
        # 画像情報をデータベースに反映する
        image_data_left = self.request.POST.get("image_data_left")
        image_data_right = self.request.POST.get("image_data_right")
        feet.foot_left = base64_file(image_data_left)
        feet.foot_right = base64_file(image_data_right)
        feet.save()
        return redirect("feet:crop-left", pk=pk)


class LeftFootsizePerspeciveCropperView(DetailView):

    """ 左足のイメージをクロップするためのツールを提供する """

    model = models.FootImage
    context_object_name = "foot_images"
    template_name = "feet/feet-cropper-left.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.FootImageDataForm()
        return context

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        # 画像情報をデータベースに反映する
        image_data = self.request.POST.get("image_data")
        processed_foot = models.ProcessedFootImage.objects.create(
            foot_left=base64_file(image_data)
        )
        self.request.session["processed_foot"] = processed_foot.pk
        return redirect("feet:crop-right", pk=pk)


class RightFootsizePerspeciveCropperView(DetailView):

    """ 右足のイメージをクロップするためのツールを提供する """

    model = models.FootImage
    context_object_name = "foot_images"
    template_name = "feet/feet-cropper-right.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.FootImageDataForm()
        return context

    def post(self, *args, **kwargs):
        processed_foot_pk = self.request.session["processed_foot"]
        # 画像情報をデータベースに反映する
        image_data = self.request.POST.get("image_data")
        processed_foot = models.ProcessedFootImage.objects.get(pk=processed_foot_pk)
        processed_foot.foot_right = base64_file(image_data)
        processed_foot.save()
        return redirect("feet:analyze", pk=processed_foot.pk)


def footsizes_analysis(request, *args, **kwargs):
    pk = kwargs.get("pk")
    product_pk = request.session["product"]
    design_pk = request.session["design"]
    instance = models.ProcessedFootImage.objects.get(pk=pk)
    foot_left = instance.foot_left
    foot_right = instance.foot_right
    # イメージから足サイズを計算する
    length_left, width_left = analyze.analyze(foot_left)
    length_right, width_right = analyze.analyze(foot_right)
    # ユーザーに足サイズデータを登録・更新する
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    # 会員に既存の足サイズデータがある場合、データを更新する
    try:
        footsize = models.Footsize.objects.get(user=user)
        footsize.length_left = length_left
        footsize.width_left = width_left
        footsize.length_right = length_right
        footsize.width_right = width_right
        footsize.save()
    # 会員に足サイズデータが存在しない場合、データを新規登録する
    except models.Footsize.DoesNotExist:
        footsize = models.Footsize.objects.create(
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
    return redirect("carts:add_cart", pk=product_pk, design_pk=design_pk)

