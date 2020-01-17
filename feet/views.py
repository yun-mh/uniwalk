from django.shortcuts import render
from django.views.generic import CreateView, View
from . import models
from products import models as product_models


class FootsizesMeasureView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get("pk")
        product = product_models.Product.objects.all().get(pk=pk)
        return render(request, "feet/feet-measure.html", {"product": product})
