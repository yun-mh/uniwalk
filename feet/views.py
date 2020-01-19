from django.shortcuts import render
from django.views.generic import CreateView, View
from designs import models as design_models
from products import models as product_models
from . import models


class FootsizesMeasureView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get("pk")
        design_pk = request.session["design"]
        product = product_models.Product.objects.all().get(pk=pk)
        design = design_models.Design.objects.get(pk=design_pk)
        return render(
            request, "feet/feet-measure.html", {"product": product, "design": design}
        )
