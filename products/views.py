from django.views.generic.base import View
from django.views.generic import ListView
from django.shortcuts import render
from . import models

# Create your views here.
class HomeView(View):

    """ HomeView Definition """

    def get(self, request):
        return render(request, "statics/home.html")


class ProductView(ListView):

    """ 商品一覧 """

    model = models.Product
    paginate_by = 9
    ordering = "created"
    context_object_name = "products"
    extra_context = {
        "category": models.Category.objects.all(),
    }
    template_name = "products/product-list.html"


class CategoryProductView(ListView):

    model = models.Product
    paginate_by = 9
    ordering = "created"
    context_object_name = "products"
    extra_context = {
        "category": models.Category.objects.all(),
    }
    template_name = "products/product-list.html"

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.kwargs.get("pk"))
