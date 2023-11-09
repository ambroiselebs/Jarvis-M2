import pyttsx3
from colorama import Fore
import os
import pyfiglet
from plyer import notification

def say(tosay: str)->bool:
  engine = pyttsx3.init()

  engine.say(tosay)
  engine.runAndWait()

  return True

def sendNotification(content: str, title: str)->bool:

  notification.notify(
    title=title,
    message=content,
    app_icon=None,
    timeout=10,
    toast=False
  )

  return True

def drawJarvis():
  os.system('cls' if os.name == 'nt' else 'clear')
  print(Fore.BLUE + pyfiglet.figlet_format("Jarvis", font="slant"))