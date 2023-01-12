import datetime
import io

import pygame
import wikipedia
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import pyttsx3
import pywhatkit

name = 'alexa'

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 145)
engine.setProperty('voice', voices[0].id)
wikipedia.set_lang('es')


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    commands = ""
    try:
        with sr.Microphone() as source:
            print("Di algo")
            voice = listener.listen(source)
            commands = listener.recognize_google(voice, language='es-MX')
            commands = ''.join(commands).lower()
            if name in commands:
                commands = commands.replace('alexa','')
                print(commands)
            else:
                talk("Por favor di mi nombre")
    except Exception as e:
        print(e)
    return commands


def main():
    try:
        while True:
            response = listen()
            if 'reproduce' in response:
                music = response.replace('reproduce', '')
                talk(f"Reproduciendo {music}")
                pywhatkit.playonyt(music)
            elif 'busca' in response:
                order = response.replace('busca','')
                info = wikipedia.summary(order,1)
                talk(info)
            elif 'hora' in response:
                hora = datetime.datetime.now().strftime("%I:%M %p")
                talk(f"Son las {hora}")
            elif 'apágate' in response:
                talk("Apagando...")
                break
    except Exception as e:
        talk(f"Lo siento no te entendi debido a este error")
        print(e)

if __name__ == '__main__':
    main()
