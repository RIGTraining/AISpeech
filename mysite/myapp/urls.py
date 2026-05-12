from django.urls import path
from . import views

urlpatterns = [
    # Meeting endpoints
    path('meetings/', views.meeting_list, name='meeting-list'),
    path('meetings/<int:pk>/', views.meeting_detail, name='meeting-detail'),
    
    # Participant endpoints
    path('meetings/<int:meeting_id>/participants/', views.meeting_participants, name='meeting-participants'),
    path('meetings/<int:meeting_id>/transcripts/', views.meeting_transcripts, name='meeting-transcripts'),
    
    path('meeting_participants_template/<int:meeting_id>/', views.meeting_participants_template, name='meeting_participants_template'),
    path('viewTranscript/<int:meeting_id>/', views.viewTranscript, name='viewTranscript'),
]