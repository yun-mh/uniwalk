from django.views.generic import View
from django.shortcuts import render
from products import models as product_models


class HomeView(View):

    """ ホーム """

    def get(self, request):
        products = product_models.Product.objects.all().order_by("-created")[:3]
        context = {"products": products}
        return render(request, "statics/home.html", context)


class AboutView(View):

    """ Uniwalk紹介 """

    def get(self, request):
        return render(request, "statics/about.html")
