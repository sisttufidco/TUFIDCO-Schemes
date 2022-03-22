from django.urls import path
from . import views

urlpatterns = [
    path('export_park', views.export_tobecommenced_xls, name='export')
]