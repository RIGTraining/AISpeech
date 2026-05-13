from django.urls import path
from . import views

urlpatterns = [
    # url endpoints
  path('upload/', views.upload_video, name='upload_video'),  
]