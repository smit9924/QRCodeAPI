from django.shortcuts import render, HttpResponse
from django.views import View

class QRScaneIndex(View):
    template_name = 'QRScane/index.html'

    def get(self, request):
        return render(request, self.template_name)
