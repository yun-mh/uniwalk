from django.shortcuts import render
from django.views.generic import ListView, DetailView
from designs import models as design_model
from reviews import models as review_model
from . import models


class ProductListView(ListView):

    """ 商品一覧 """

    model = models.Product
    paginate_by = 9
    context_object_name = "products"
    extra_context = {
        "count": len(models.Product.objects.all()),
        "categories": models.Category.objects.all(),
    }
    template_name = "products/product-list.html"

    def get_queryset(self):
        if self.kwargs.get("pk"):
            return models.Product.objects.filter(
                category_id=self.kwargs.get("pk")
            ).order_by("-created")
        return models.Product.objects.all().order_by("-created")


class ProductDetailView(DetailView):

    """ 商品詳細 """

    model = models.Product
    template_name = "products/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        designs = self.object.design.all().exclude(user__isnull=True)
        design_list = sorted(
            designs, key=lambda design: design.total_likes, reverse=True
        )[0:4]
        posts = self.object.reviews.all().order_by("-created")[0:4]
        each = {review.pk: review.text for review in posts}
        context["reviews_text"] = each
        context["rev"] = posts
        context["designs"] = design_list
        context["count_designs"] = designs
        return context
