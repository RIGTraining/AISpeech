from django.shortcuts import render
from django.http import JsonResponse
from .models import Video


def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        video_file = request.FILES.get('video')

        if not title or not video_file:
            return JsonResponse({'error': 'Title and video file are required.'}, status=400)

        video = Video.objects.create(title=title, summary=summary, video=video_file)
        return JsonResponse({'message': 'Video uploaded successfully.', 'video_id': video.id, 'success': True})
    elif request.method == 'GET':
        videos = Video.objects.all().values('id', 'title', 'summary', 'video', 'uploaded_at')
        return JsonResponse({'videos': list(videos)}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)







