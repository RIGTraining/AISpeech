from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_video, name='upload'),
    path('result/<int:pk>/', views.result, name='result'),
]