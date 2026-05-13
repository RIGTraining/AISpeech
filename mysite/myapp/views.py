import json

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from .models import Meeting, MeetingParticipant, MeetingTranscript
from .serializers import *
from django.shortcuts import render

# ==================== MEETING VIEWS ====================
@api_view(['GET', 'POST'])
def meeting_list(request):
    if request.method == 'GET':
        meetings = Meeting.objects.all().order_by('-created_at')
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def meeting_detail(request, pk):
    try:
        meeting = Meeting.objects.get(pk=int(pk))
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeetingSerializer(meeting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print('Deleting meeting:', meeting.title)
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ==================== update meeting =====================

# meeting participants 
#MeetingParticipantSerializer
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def meeting_participants(request, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=int(meeting_id))
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        participants = MeetingParticipant.objects.filter(meeting=meeting)
        serializer = MeetingParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['meeting'] = meeting.id
        serializer = MeetingParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        participant_id = request.data.get('participant')
        if not participant_id:
            return Response({'error': 'Participant ID is required for update.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            participant = MeetingParticipant.objects.get(id=int(participant_id))
        except MeetingParticipant.DoesNotExist:
            return Response({'error': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MeetingParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        participant_id = json.loads(request.body).get('participant_id')
        if not participant_id:
            return Response({'error': 'Participant ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            participant = MeetingParticipant.objects.get(id=int(participant_id))
        except MeetingParticipant.DoesNotExist:
            return Response({'error': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)
        participant.delete()
        return Response({'message': 'Participant deleted successfully.'})

@api_view(['GET', 'POST'])
def meeting_transcripts(request, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=int(meeting_id))
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        transcripts = MeetingTranscript.objects.filter(meeting=meeting)
        serializer = MeetingTranscriptSerializer(transcripts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['meeting'] = meeting.id
        serializer = MeetingTranscriptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#================= Template Views ====================
def meeting_participants_template(request, meeting_id):
    print('helo')
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    participants = MeetingParticipant.objects.filter(meeting=meeting)
    return render(request, 'participants.html', {'meeting': meeting, 'participants': participants})


def viewTranscript(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    transcripts = MeetingTranscript.objects.filter(meeting=meeting)
    return render(request, 'viewTranscriptEdit.html', {'meeting': meeting, 'transcripts': transcripts})