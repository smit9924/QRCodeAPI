from django.contrib import admin
from django.urls import path
from QRScane import views

urlpatterns = [
    path('', views.QRScaneIndex.as_view(), name='index_page'),
]