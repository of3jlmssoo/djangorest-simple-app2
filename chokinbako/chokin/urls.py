from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.chokin, name='chokin'),
    # path('confirm/<price>/<box>/<proc>/', views.confirm, name='confirm'),
    path('confirm/<int:thousands>/<int:millions>', views.confirm, name='confirm'),
    path('resetchokin', views.resetchokin, name='resetchokin'),
    path('select_box/<int:id>', views.select_box, name='select_box'),
    path('select_proc/<int:id>', views.select_proc, name='select_proc'),
    path('proc_bill/<str:target>/<str:proc>', views.proc_bill, name='proc_bill'),
]
