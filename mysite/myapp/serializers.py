from rest_framework import serializers
from .models import Meeting, MeetingParticipant, MeetingTranscript

class MeetingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingParticipant
        fields = ['id', 'meeting', 'participant']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MeetingTranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTranscript
        fields = ['id', 'meeting', 'participant', 'transcript', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'schedule_date']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MeetingDetailSerializer(serializers.ModelSerializer):
    participants = MeetingParticipantSerializer(many=True, read_only=True)
    transcripts = MeetingTranscriptSerializer(many=True, read_only=True)
    
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'schedule_date', 
                 'created_at', 'updated_at', 'participants', 'transcripts']