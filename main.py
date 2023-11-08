import speech_recognition as sr
import pyttsx3
import pygame
import pygame
# Commands import
import commands.all as c
import commands.gpt as gpt
import commands.debug as debug

r = sr.Recognizer()

# Commands
Commands = {
    # WEATHER COMMANDS
    "température": c.get_weather,
    "c'est comment dehors": c.get_weather,
    # TIME COMMANDS
    "l'heure": c.get_date,
    "il est quelle heure": c.get_date,
    # WORK COMMANDS
    "j'ai quoi à faire": c.get_homework,
    # GOODNIGHT COMMAND
    "bonne nuit": c.say_goodnight
}

# SETUP
pygame.init()

# GREET THE USER
if debug.DEBUG_STATUS:
    engine = pyttsx3.init()
    pygame.mixer.init()

    pygame.mixer.music.load("sounds/openning.mp3")
    pygame.mixer.music.play()
    engine.say(f"Bonjour monsieur, {c.get_date()}, {c.get_weather()}. Que puis-je faire pour vous ?")
    engine.runAndWait()

    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.stop()

    print(debug.DEBUG_FORMAT + "Done greeting the user")
else:
    print(debug.DEBUG_FORMAT + "Starting Jarvis in dev mode")


# Listening for audio
def get_audio():
    # With microphone
    if not debug.DEBUG_MIC:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Adjusting for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.2)
            print(debug.DEBUG_FORMAT + "Waiting for Jarvis...")

            # Listening for audio
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                print(f"{debug.DEBUG_FORMAT}| '{text}'")
                return text
            except sr.UnknownValueError:
                print(debug.DEBUG_FORMAT + "Understanding error")
                return ""
            except sr.RequestError as e:
                print(debug.DEBUG_FORMAT + "Request error")
                return ""
            
    # With input()
    else:
        text = input("Jarvis : ")
        return text



# MAIN LOOP
while True:
    while True:
        audio = get_audio()

        # Start Jarvis
        if audio == "Jarvis":
            print(debug.DEBUG_FORMAT + "Jarvis enclanched : Waiting for command...")
            break

        # Stop Jarvis
        elif "stop" in audio or "stoppe" in audio:
            engine = pyttsx3.init()
            engine.say("Arret d'urgence enclanché")
            engine.runAndWait()
            print(debug.DEBUG_FORMAT + "STOPPING")
            exit()

    if __name__ == '__main__':
        engine = pyttsx3.init()
        engine.say("Je vous écoute monsieur")
        engine.runAndWait()

        # Listening for commands
        while True:
            audio = get_audio()

            # COMMANDS
            if audio.lower() in Commands:
                engine.say(Commands[audio.lower()]())
                engine.runAndWait()

                break

            # AI COMMANDS
            elif len(audio) > 0 and audio.lower() not in Commands:
                engine.say("Un instant je vous prie")
                engine.runAndWait()

                response = gpt.ai(audio)
                break

            # Don't do anything if the user didn't say anything
            else:
                print(debug.DEBUG_FORMAT + "Waiting for command")
