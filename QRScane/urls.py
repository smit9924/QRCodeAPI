from django.contrib import admin
from django.urls import path
from QRScane import views

urlpatterns = [
    path('', views.QRScaneIndex.as_view(), name='index_page'),
    path('StartScanning/', views.StartScanning.as_view(), name='Start the scanning of the qr code'),
]
