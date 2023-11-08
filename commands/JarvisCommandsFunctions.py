import requests
import os
import datetime
from dotenv import load_dotenv
import pronotepy
from pronotepy.ent import l_normandie
import pygame
import pyttsx3
import commands.JarvisSettings as JarvisSettings
from plyer import notification

load_dotenv()


# Goodnight
def say_goodnight() -> any:
    engine = pyttsx3.init()
    pygame.mixer.init()

    pygame.mixer.music.load("sounds/closing.mp3")
    pygame.mixer.music.play()

    engine.say("Bonne nuit monsieur")
    engine.runAndWait()

    while pygame.mixer.music.get_busy():
        continue

    print(JarvisSettings.DEBUG_FORMAT + "Stopping")
    pygame.mixer.music.stop()
    exit()


# Get the weather
def get_weather() -> str:
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Sotteville-les-Rouen,fr&units=metric&lang=fr&appid=' + os.getenv(
        'OPEN_WEATHER_KEY')
    response = requests.get(url)
    data = response.json()

    # Extrait les informations de température et de météo à partir des données JSON
    temp = data['main']['temp']
    weather = data['weather'][0]['description']

    notification.notify(
        title='Jarvis',
        message=f"Température : {round(temp)} degrés. Temps {weather}.",
        app_icon=r'jarvis.ico',
        timeout=10,
    )
    return f"La température à Sotteville lès Rouen est de {round(temp)} degrés. Le temps est {weather}."


# Get the current date and time
def get_date() -> str:
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    heure = now.strftime("%H")
    minute = now.strftime("%M")
    return "Nous sommes le : " + str(date) + ", et il est : " + str(heure) + "heure, " + str(minute)


# Get my homework from Pronote
def get_homework() -> list:
    D = []
    client = pronotepy.Client(os.getenv('ent_url'),
                              username=os.getenv('ENT_USERNAME'),
                              password=os.getenv('ENT_PASSWORD'),
                              ent=l_normandie)

    for home in client.homework(datetime.date.today()):
        if f"Pour le {home.date}, en {home.subject.name} : {home.description}." not in D:
            D.append(f"Pour le {home.date}, en {home.subject.name} : {home.description}.")

    print(D)
    return D
