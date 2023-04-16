from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('payment/<str:title>/', views.payment, name='payment'),
    path('payment/<str:title>/', views.show_game, name='payment'),
]