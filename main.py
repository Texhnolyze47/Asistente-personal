import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import pyttsx3
import pywhatkit

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 145)
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Di algo")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path,format='wav')
    except Exception as e:
        print(e)
    return save_path

def recongize_audio(save_path):
    audio_model = whisper.load_model('base')
    transcription = audio_model.transcribe(save_path, language='spanish',fp16=False)
    return transcription['text']


def main():

    try:
        response = recongize_audio(listen()).lower()
        talk(response)
        #print(response)
        if 'reproduce' in response:
            music = response.replace('reproduce','')
            talk(f"Reproduciendo {music}")
            pywhatkit.playonyt(music)
    except Exception as e:
        talk(f"Lo siento no te entendi debido a este error: {e}")
        print(e)

if __name__ == '__main__':
    main()