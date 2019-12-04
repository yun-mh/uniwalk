from django.views.generic import ListView, View, DetailView
from django.shortcuts import render
from reviews import models as review_model
from . import models

# Create your views here.
class HomeView(View):

    """ HomeView Definition """

    def get(self, request):
        return render(request, "statics/home.html")


class ProductListView(ListView):

    """ 商品一覧 """

    model = models.Product
    paginate_by = 9
    ordering = "created"
    context_object_name = "products"
    extra_context = {
        "categories": models.Category.objects.all(),
    }
    template_name = "products/product-list.html"

    def get_queryset(self):
        if self.kwargs.get("pk"):
            return models.Product.objects.filter(category_id=self.kwargs.get("pk"))
        return models.Product.objects.all()


class ProductDetailView(DetailView):

    """ 商品詳細 """

    model = models.Product
    template_name = "products/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.reviews.all()
        each = [review.text for review in posts]
        context["reviews_text"] = each
        context["rev"] = self.object.reviews.all()
        return context

