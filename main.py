import speech_recognition as sr
import pyttsx3
import pygame
import pygame
# Commands import
import commands.JarvisPublicFunctions as JarvisPublicFunctions
import commands.JarvisCommandsFunctions as JarvisCommandsFunctions
import commands.JarvisIAFunctions as JarvisIAFunctions
import commands.JarvisSettings as JarvisSettings

r = sr.Recognizer()

# Commands
Commands = {
    # WEATHER COMMANDS
    "température": JarvisCommandsFunctions.get_weather,
    "c'est comment dehors": JarvisCommandsFunctions.get_weather,
    # TIME COMMANDS
    "l'heure": JarvisCommandsFunctions.get_date,
    "il est quelle heure": JarvisCommandsFunctions.get_date,
    # WORK COMMANDS
    "j'ai quoi à faire": JarvisCommandsFunctions.get_homework,
    # GOODNIGHT COMMAND
    "bonne nuit": JarvisCommandsFunctions.say_goodnight
}

# SETUP
pygame.init()
JarvisPublicFunctions.drawJarvis()

# GREET THE USER
if JarvisSettings.DEBUG_STATUS:

    engine = pyttsx3.init()
    pygame.mixer.init()

    pygame.mixer.music.load("sounds/openning.mp3")
    pygame.mixer.music.play()

    JarvisPublicFunctions.say(f"Bonjour monsieur, {JarvisCommandsFunctions.get_date()}, {JarvisCommandsFunctions.get_weather()}. Que puis-je faire pour vous ?")

    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.stop()

    print(JarvisSettings.DEBUG_FORMAT + "Done greeting the user")
else:
    print(JarvisSettings.DEBUG_FORMAT + "Starting Jarvis in dev mode")


# Listening for audio
def get_audio():
    # With microphone
    if not JarvisSettings.DEBUG_MIC:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Adjusting for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.2)
            print(JarvisSettings.DEBUG_FORMAT + "Waiting for Jarvis...")

            # Listening for audio
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                print(f"{JarvisSettings.DEBUG_FORMAT}| '{text}'")
                return text
            except sr.UnknownValueError:
                print(JarvisSettings.DEBUG_FORMAT + "Understanding error")
                return ""
            except sr.RequestError as e:
                print(JarvisSettings.DEBUG_FORMAT + "Request error")
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
            print(JarvisSettings.DEBUG_FORMAT + "Jarvis enclanched : Waiting for command...")
            break

        # Stop Jarvis
        elif "stop" in audio or "stoppe" in audio:
            JarvisPublicFunctions.say("Arret d'urgence enclanché")

            print(JarvisSettings.DEBUG_FORMAT + "STOPPING")
            exit()

    if __name__ == '__main__':
        JarvisPublicFunctions.say("Je vous écoute monsieur")

        # Listening for commands
        while True:
            audio = get_audio()

            # COMMANDS
            if audio.lower() in Commands:
                JarvisPublicFunctions.say(Commands[audio.lower()]())

                break

            # AI COMMANDS
            elif len(audio) > 0 and audio.lower() not in Commands:
                JarvisPublicFunctions.say("Un instant je vous prie")
                response = JarvisIAFunctions.ai(audio)
                break

            # Don't do anything if the user didn't say anything
            else:
                print(JarvisSettings.DEBUG_FORMAT + "Waiting for command")
