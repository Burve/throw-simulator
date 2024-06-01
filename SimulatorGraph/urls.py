from django.urls import path
from . import views

urlpatterns = [
    path('', views.simulation, name='simulation'),
    path('download_plot/', views.download_plot, name='download_plot'),
]