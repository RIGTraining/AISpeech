from django.db import models

class Video(models.Model):

    title = models.CharField(max_length=255)

    summary = models.TextField()

    video = models.FileField(upload_to='videos/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Create your models here.
class VideoUpload(models.Model):
    video = models.FileField(upload_to='videos/')
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} - {self.uploaded_at}"
