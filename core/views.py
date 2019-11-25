from django.views.generic import View
from django.shortcuts import render

# Create your views here.
class AboutView(View):
    def get(self, request):
        return render(request, "statics/about.html")
