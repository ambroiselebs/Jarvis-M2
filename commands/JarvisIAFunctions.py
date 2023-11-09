from shuttleai import *
import pyttsx3
import commands.JarvisSettings as JarvisSettings
import requests
import json
import os
from plyer import notification
import requests
import random

# Initializing GPT-3 + DALL-E + pyttsx3
shuttle = ShuttleClient(api_key=os.getenv("OPENAI_KEY"))
engine = pyttsx3.init()
chat = [{
    'role': 'system',
    'content': 'you are a voice assistant named Jarvisse. Don t present yourself at each message, just one time it s enough. Never use emojis'
}]

def ai(query: str) -> str:  
    # DALLE-E
    if "crée-moi" in query or "génère-moi" in query or "génère" in query or "génère-moi" in query and ("image" in query or "images" in query):
        print(JarvisSettings.DEBUG_FORMAT + "DALL-E's gonna answer for this one")

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
            # Printing image link
            print(res)

            # create folder images/ if it doesn't exist
            if not os.path.exists("images/"):
                os.mkdir("images/")
            # Saving image to images/file_name
            random_number = random.randint(0, 100000)
            image_url = res['data'][0]['url']
            image_name = "images/"+image_url.split("/")[-1]+"-"+str(random_number)+".png"
            image = requests.get(image_url)
            with open(image_name, "wb") as f:
                f.write(image.content)

            # Send a notification to the user with the image link
            notification.notify(
                title="Jarvis",
                message=f"L'image a bien été générée. Elle est disponible dans le dossier images sous le nom {image_name.split('/')[-1]}",
                app_icon="jarvis.ico",
                timeout=10
            )
            # saying the image has been generated
            engine.say("L'image a bien été générée")
            engine.runAndWait()

            return "ok"
        else: 
            print(f"{JarvisSettings.DEBUG_FORMAT}Error: {res}")
            engine.say("Une erreur est survenue")
            engine.runAndWait()
            return f"{JarvisSettings.DEBUG_FORMAT}Error: {res.status_code}" """ """

    # GPT-3.5-TURBO
    else:

        # Clearing chat
        if "changeons de conversation" in query or "change de conversation" in query or "efface les autres messages" in query:
            chat.clear()
            chat.append({
                'role': 'system',
                'content': 'you are a voice assistant named Jarvisse. Don t present yourself at each message, just one time it s enough. Never use emojis'
            })
            engine.say("Ok, changeons de conversation")
            engine.runAndWait()
            return "cleared"
        
        # Sending message to GPT-3.5-TURBO
        else:
            print(JarvisSettings.DEBUG_FORMAT + "GPT3's gonna answer for this one")
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

            # create folder responses/ if it doesn't exist
            if not os.path.exists("responses/"):
                os.mkdir("responses/")

            # Saving answer if 'enregistre la réponse' in query in a file called 'answers.txt'+random_number in the folder 'responses/'
            if "enregistre la réponse" in query:
                random_number = random.randint(0, 100000)
                with open("responses/"+query[3:]+".txt", "w") as f:
                    f.write(msg.encode("utf-8"))
                engine.say("La réponse a bien été enregistrée")
                engine.runAndWait()
                return "ok"

            engine.say(msg)
            engine.runAndWait()

            return msg

       