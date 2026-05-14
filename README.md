# AISpeech

pip install speechrecognition pydub


pip install openai-whisper

pip install torch

pip install moviepy==1.0.3


google - gemma 4 - speech to text


from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content(
    model="gemma-4-31b-it",
    contents="Explain the benefits of Gemma 4's multimodal native architecture."
)
print(response.text)
