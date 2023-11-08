import pyttsx3
from colorama import Fore
import os
import pyfiglet

def say(tosay: str)->bool:
  engine = pyttsx3.init()

  engine.say(tosay)
  engine.runAndWait()

  return True

def drawJarvis():
  os.system('cls' if os.name == 'nt' else 'clear')
  print(Fore.BLUE + pyfiglet.figlet_format("Jarvis", font="slant"))