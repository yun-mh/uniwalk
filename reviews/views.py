from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, View, DetailView, FormView
from products import models as product_models
from users import mixins
from . import models, forms


class ReviewListView(ListView):

    """ レビュー一覧 """

    model = models.Review
    paginate_by = 5
    context_object_name = "reviews"
    template_name = "reviews/review-list.html"

    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs.get("pk")).order_by(
            "-created"
        )

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        product = product_models.Product.objects.all().filter(pk=pk)[0]
        context["product"] = product
        return context


class ReviewPostView(mixins.LoggedInOnlyView, FormView):

    """ レビュー投稿 """

    template_name = "reviews/review-post.html"
    success_url = reverse_lazy("products:detail")
    form_class = forms.ReviewForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        product = product_models.Product.objects.all().filter(pk=pk)[0]
        context["product"] = product
        return context

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        product = product_models.Product.objects.get(pk=pk)
        review = form.save()
        review.product = product
        review.user = self.request.user
        review.save()
        messages.success(self.request, _("レビューを投稿しました。"))
        return redirect(reverse("products:detail", kwargs={"pk": pk}))