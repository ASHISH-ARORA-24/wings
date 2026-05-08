from django.urls import path
from . import views

app_name = 'family'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
