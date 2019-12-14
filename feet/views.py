from django.shortcuts import render
from django.views.generic import CreateView, View
from . import models


class FootsizesMeasureView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        return render(request, "feet/feet-measure.html")
