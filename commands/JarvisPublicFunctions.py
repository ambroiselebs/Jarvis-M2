import pyttsx3

def say(tosay: str):
  engine = pyttsx3.init()

  engine.say(tosay)
  engine.runAndWait()