from django.shortcuts import render, HttpResponse
from django.views import View

class QRGenerateIndex(View):
    template_name = 'QRGenerate/index.html'

    def get(self, request):
        return render(request, self.template_name)
