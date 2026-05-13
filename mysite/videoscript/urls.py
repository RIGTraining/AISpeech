from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    # url endpoints
  path('upload/', views.upload_video, name='upload_video'),  
=======
    path('', views.upload_video, name='upload'),
    path('result/<int:pk>/', views.result, name='result'),
>>>>>>> ae38888fc89a007c60437c54139567cb37dd73d1
]