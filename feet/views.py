from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from designs import models as design_models
from products import models as product_models
from . import models, forms


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
                length_right = footsize_fill_form.cleaned_data.get("length_right")
                width_left = footsize_fill_form.cleaned_data.get("width_left")
                width_right = footsize_fill_form.cleaned_data.get("width_right")
                # 既存の足サイズデータがある場合、データを更新する
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
                foot_pk = footsize.pk
                return redirect(
                    "carts:add_cart", pk=pk, design_pk=design_pk, foot_pk=foot_pk
                )
            footsize_image_form = forms.FootsizeImageForm(prefix="image")
        elif "footsize-image" in request.POST:
            footsize_image_form = forms.FootsizeImageForm(
                request.POST, request.FILES, prefix="image"
            )
            if footsize_image_form.is_valid():
                foot_images = models.FootImage(
                    length_left=request.FILES["image-length_left"],
                    length_right=request.FILES["image-length_right"],
                    width_left=request.FILES["image-width_left"],
                    width_right=request.FILES["image-width_right"]
                )
                foot_images.save()
                return redirect("feet:auto", pk=foot_images.pk)
            footsize_fill_form = forms.FootsizeFillForm(prefix="fill")
    else:
        footsize_fill_form = forms.FootsizeFillForm(prefix="fill")
        footsize_image_form = forms.FootsizeImageForm(prefix="image")
    context = {
        "footsize_fill_form": footsize_fill_form,
        "footsize_image_form": footsize_image_form,
    }
    return render(request, "feet/feet-measure.html", context)


def footsizes_auto(request, *args, **kwargs):
    pk = kwargs.get("pk")
    instance = models.FootImage.objects.get(pk=pk)
    length_left = instance.length_left
    width_left = instance.width_left
    length_right = instance.length_right
    width_right = instance.width_right