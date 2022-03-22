from django.urls import path
from . import views

urlpatterns = [
    path('export_park_xls/', views.park_export_xls, name='export_park'),
]
