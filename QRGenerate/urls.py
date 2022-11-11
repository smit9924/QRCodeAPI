from django.contrib import admin
from django.urls import path
from QRGenerate import views

urlpatterns = [
    path('', views.QRGenerateIndex.as_view(), name='index_page_qrgenerate'),
    path('MakeQR/<email>/<path:aligibility>', views.QRGenerator.as_view(), name='QR_Code_generator'),
    path('MakeQR/ThanganatQRCodeGenerator/<password>/<email>/<id>', views.ThanganatQRCodeGenerate.as_view(), name='Thanganat_QR_Code_generator'),
]
