from django import forms
from .models import VideoUpload

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['video']
        widgets = {
            'video': forms.FileInput(attrs={'accept': 'video/*'})
        }