from django.urls import path
from . import views

urlpatterns = [
    path('', views.transcribe_view, name='transcribe'),
]