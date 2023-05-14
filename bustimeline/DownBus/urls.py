from django.urls import path
from .views import busListView

urlpatterns = [
    path('buslist/', busListView, name='bus-list'),
]
