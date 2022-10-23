from django.shortcuts import render, HttpResponse
from django.views import View

class index(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
