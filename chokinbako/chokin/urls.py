from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.chokin, name='chokin'),
    # path('confirm/<price>/<box>/<proc>/', views.confirm, name='confirm')
    path('confirm', views.confirm, name='confirm')
]
