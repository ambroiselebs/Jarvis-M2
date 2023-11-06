import openai
import pyttsx3
import os
from colorama import Fore

# OpenAI setup
openai.api_key = os.getenv('OPENAI_KEY')
openai.api_base = os.getenv('OPENAI_URL')
chat = [{
    'role': 'system',
    'content': 'you are a voice assistant named Jarvisse. Please never give me links of website just answer the question with human like sentence or if needed code exemple. Don t present yourself at each message, just one time it s enough.'
}]

# Text to speach setup
engine = pyttsx3.init()


# GPT3 function
def gpt3(query: str) -> str:
    if query == "" or query == " ":
        print(Fore.RED + "[ERROR]" + Fore.RESET + " No query specified")
        return ""
    else:
        chat.append({'role': 'user', 'content': query})
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=chat,
        )
        msg = res.choices[0].message['content']

        # Parse msg to remove links
        toRead = ""
        parsedMsg = msg.split("\n")
        for line in parsedMsg:
            if "http" not in line or "https" not in line:
                toRead += line

        # Read response
        # engine.say(toRead.replace("*", ""))
        # engine.runAndWait()

        # Check if code or no
        if "```" in toRead:
            # Save code inside ``` ``` to a file create it if not exist
            print(toRead.split("```"), sep="\n")
            code = toRead.split("```")[1]
            fileName = code.split(" ")[0]
            print(code)
            # create file
            if not os.path.exists("code"):
                os.mkdir("code")
            try:
                with open(f"code/{fileName}.txt", "w+") as f:
                    f.write(code + "\n")
            except Exception as e:
                print(Fore.RED + "[ERROR]" + Fore.RESET + f"An error occurred: {str(e)}")

            engine.say("J'ai envoyé le resultat sur votre ordinateur")
            engine.runAndWait()

        else:
            engine.say(toRead.replace("*", ""))
            engine.runAndWait()

        return msg
