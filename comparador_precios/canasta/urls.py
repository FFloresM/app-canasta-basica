from django.urls import path
from . import views

app_name = 'canasta'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:prod>/buscar/', views.buscar, name='buscar'),
]