# import moviepy.editor as mp

import speech_recognition as sr
from django.shortcuts import render, redirect
from django.conf import settings
from .models import VideoUpload
from .forms import VideoUploadForm
import os
# from moviepy.editor import VideoFileClip

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_obj = form.save()

            # Process video
            try:
                # Extract audio
                video_path = video_obj.video.path
                audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', f"{video_obj.id}.wav")
                
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)

                # video = VideoFileClip(video_path)
                # video.audio.write_audiofile(audio_path)

                # # Speech Recognition
                # recognizer = sr.Recognizer()
                # with sr.AudioFile(audio_path) as source:
                #     audio_data = recognizer.record(source)
                #     text = recognizer.recognize_google(audio_data)

                # video_obj.transcript = text
                # video_obj.audio = f'audio/{video_obj.id}.wav'
                # video_obj.save()

                return redirect('result', pk=video_obj.pk)

            except Exception as e:
                video_obj.transcript = f"Error: {str(e)}"
                video_obj.save()

    else:
        form = VideoUploadForm()

    return render(request, 'core/upload.html', {'form': form})


def result(request, pk):
    video = VideoUpload.objects.get(pk=pk)
    return render(request, 'core/result.html', {'video': video})