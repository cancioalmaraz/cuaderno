from django.urls import path
from . import views

urlpatterns = [
    path('<int:ot>/', views.index, name = "home"),
    path('plot/<int:oj>/', views.graph, name = "graph"),
]