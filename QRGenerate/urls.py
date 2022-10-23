from django.contrib import admin
from django.urls import path
from QRGenerate import views

urlpatterns = [
    path('', views.index.as_view(), name='index_page'),
]
