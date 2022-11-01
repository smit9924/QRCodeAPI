from django.contrib import admin
from django.urls import path
from QRScane import views

urlpatterns = [
    path('', views.QRScaneIndex.as_view(), name='index_page'),
    path('StartScanning/', views.StartScanning.as_view(), name='Start_the_scanning_of_the_qr_code'),
    path('ajaxCall', views.AjaxCall.as_view(), name='Start_the_scanning_of_the_qr_code'),
]
