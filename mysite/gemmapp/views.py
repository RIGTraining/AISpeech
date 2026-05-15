import tempfile
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import torch
from transformers import AutoProcessor, AutoModelForMultimodalLM
import librosa
import soundfile as sf

# Load model once (globally or in a singleton)
MODEL_ID = "google/gemma-4-E4B-it"  # or E2B-it for smaller/faster
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForMultimodalLM.from_pretrained(
    MODEL_ID, 
    device_map="auto", 
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
)

def preprocess_audio(audio_file):
    """Convert WebM → proper format for Gemma (mono, 16kHz, float32 [-1,1])"""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        # Use ffmpeg via librosa or subprocess for conversion
        y, sr = librosa.load(audio_file, sr=16000, mono=True)
        sf.write(tmp.name, y, sr)
        return tmp.name

@csrf_exempt
def transcribe_view(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        
        try:
            wav_path = preprocess_audio(audio_file)
            
            # Prepare prompt (follow Gemma 4 recommendations)
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": (
                        "Transcribe the following speech segment in its original language. "
                        "Only output the transcription, with no newlines. "
                        "When transcribing numbers, write the digits."
                    )},
                    {"type": "audio", "audio": wav_path},  # Processor handles loading
                ]
            }]
            
            inputs = processor.apply_chat_template(
                messages, 
                add_generation_prompt=True,
                tokenize=True, 
                return_dict=True,
                return_tensors="pt"
            ).to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs, 
                    max_new_tokens=256,  # Adjust based on expected length
                    do_sample=False
                )
            
            transcript = processor.batch_decode(
                outputs, 
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )[0].strip()
            
            # Clean up
            os.unlink(wav_path)
            
            return JsonResponse({'transcript': transcript})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'No audio provided'}, status=400)