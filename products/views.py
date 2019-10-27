from django.views.generic.base import View
from django.shortcuts import render

# Create your views here.
class HomeView(View):

    """ HomeView Definition """
    
    def get(self, request):
        return render(request, "statics/home.html")