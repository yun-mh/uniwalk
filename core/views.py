from django.views.generic import View
from django.shortcuts import render


class HomeView(View):

    """ ホーム """

    def get(self, request):
        return render(request, "statics/home.html")
        

class AboutView(View):

    """ Uniwalk紹介 """

    def get(self, request):
        return render(request, "statics/about.html")
