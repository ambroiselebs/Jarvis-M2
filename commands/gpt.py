from shuttleai import *
import pyttsx3
import commands.debug as debug
import requests
import json
import os
from plyer import notification

# Initializing GPT-3 + DALL-E + pyttsx3
shuttle = ShuttleClient(api_key=os.getenv("OPENAI_KEY"))
engine = pyttsx3.init()

chat = [{
    'role': 'system',
    'content': 'you are a voice assistant named Jarvisse. Don t present yourself at each message, just one time it s enough.'
}]

def ai(query: str) -> str:  
    # DALLE-E
    if "image" in query or "images" in query and "créer" in query or "générer" in query or "crée-moi" in query or "génère-moi" in query or "génère" in query or "crée" in query or "génère-moi" in query:
        print(debug.DEBUG_FORMAT + "DALL-E's gonna answer for this one")

        api_key = os.getenv("OPENAI_KEY")
        api_base = "https://api.shuttleai.app/v1/images/generations"

        headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
        data = {
            "model": "kandinsky-2.2",
            "prompt": query,
            "n": 1
        }

        res = requests.post(api_base, headers=headers, json=data)
        if res.status_code == 200:
            res = json.loads(res.text)
            engine.say("L'image a bien été générée")
            engine.runAndWait()

            # Printing image link
            print(res)
            # Send a notification to the user with the image link
            notification.notify(
                title="Jarvis",
                message=f"Voici le lien de l'image générée : {res['data'][0]['url']}",
                app_icon="jarvis.ico",
                timeout=10
            )

            return "ok"
        else: 
            print(f"{debug.DEBUG_FORMAT}Error: {res}")
            engine.say("Une erreur est survenue")
            engine.runAndWait()
            return f"{debug.DEBUG_FORMAT}Error: {res.status_code}"

    # GPT-3.5-TURBO
    else:

        # Clearing chat
        if query == "changeons de conversation" or "change de conversation" or "efface les autres messages":
            chat.clear()
            chat.append({
                'role': 'system',
                'content': 'you are a voice assistant named Jarvisse. Don t present yourself at each message, just one time it s enough.'
            })
            engine.say("Ok, changeons de conversation")
            engine.runAndWait()
            return "cleared"
        

        # Sending message to GPT-3.5-TURBO
        print(debug.DEBUG_FORMAT + "GPT3's gonna answer for this one")
        chat.append({'role': 'user', 'content': query})

        res = shuttle.chat_completion(
            model="gpt-3.5-turbo",
            messages=chat,
            stream=False,
            plain=False,
            image=None,
            citations=False
        )
        msg = res['choices'][0]['message']['content']
        print(msg)

        engine.say(msg)
        engine.runAndWait()

        return msg