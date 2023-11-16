from shuttleai import *
import pyttsx3
import commands.JarvisSettings as JarvisSettings
import commands.JarvisPublicFunctions as JarvisPublicFunctions
import requests
import json
import os
import requests
import random

# Initializing GPT-3 + DALL-E + pyttsx3
shuttle = ShuttleClient(api_key=os.getenv("OPENAI_KEY"))
engine = pyttsx3.init()
chat = [{
    'role': 'system',
    'content': 'you are a voice assistant named Jarvisse. Don t present yourself at each message, just one time it s enough. Never use emojis'
}]
oldChats = []
    
def dalle(query: str) -> str:
    # Sending message to DALLE-E
    print(f"{JarvisSettings.DEBUG_FORMAT}Dalle will handle this")

    res = shuttle.images_generations(
        model="kandinsky-2.2",
        prompt=query,
        n=1,
    )

    # Checking for errors
    if "[ShuttleAI]" in res['data']:
        return "error"
    
    return res['data'][0]['url']
    

def gpt(query: str) -> str:
    # Sending message to GPT-3.5-TURBO
    print(f"{JarvisSettings.DEBUG_FORMAT}GPT-3.5-TURBO will handle this")
    chat.append({'role': 'user', 'content': query})

    res = shuttle.chat_completion(
        model="gpt-3.5-turbo-1106",
        messages=chat,
        stream=False,
        plain=False,
        image=None,
        citations=False
    )
    msg = res['choices'][0]['message']['content']
    print(msg)

    # Checking for errors
    if "[ShuttleAI] Error:" in msg:
        return "error"

    return msg

def ai(query: str) -> str:  
    print(f"{JarvisSettings.DEBUG_FORMAT}Ai will handle this")

    # DALLE-E
    if "crée-moi" in query or "génère-moi" in query or "génère" in query or "génère-moi" in query and ("image" in query or "images" in query):
        response = dalle(query)
        if response != "error":
            # Saving image to images/file_name
            random_number = random.randint(0, 100000)
            image_url = response
            image_name = "images/"+query[:40]+".png"
            image = requests.get(image_url)

            f = open(image_name, "wb")
            f.write(image.content)
            f.close()

        engine.say("L'image a bien été générée")
        engine.runAndWait()
        # Send a notification to the user with the image link
        JarvisPublicFunctions.sendNotification("L'image a bien été générée", "Jarvis")

        return "ok"

    # GPT-3.5-TURBO
    else:

        # Clearing chat
        if "changeons de conversation" in query or "change de conversation" in query or "efface les autres messages" in query:
            
            # Saving old chat
            oldChats = chat
            
            # Clearing chat
            chat.clear()
            chat.append({
                'role': 'system',
                'content': 'you are a voice assistant named Jarvisse. Don t present yourself at each message, just one time it s enough. Never use emojis'
            })
            engine.say("Ok, changeons de conversation")
            engine.runAndWait()
            return "cleared"
        
        # Getting old chat
        elif "reprends la conversation d'avant" in query:   
            chat = oldChats

            engine.say("Ok, reprenons la conversation d'avant")
            engine.runAndWait()

            return "restored"

        # Sending message to GPT-3.5-TURBO
        else:
            response = gpt(query)
            if response == "error": return "error"

            # Check if it need to be in a file
            if "enregistre la réponse" in query or "enregistre le résultat" in query:
                f = open(f"responses/{query[:20]}.txt", "w", encoding="utf-8")
                f.write(str(response))
                f.close()

                # Sending notification to the user
                JarvisPublicFunctions.sendNotification("La réponse a bien été enregistrée", "Jarvis")

                # Say that the answer has been saved
                engine.say("La réponse a bien été enregistrée")
                engine.runAndWait()

                return "ok"
            else:
                engine.say(response)
                engine.runAndWait()

                return "ok"
       