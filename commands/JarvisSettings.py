from colorama import Fore
import os

# DEBUG
DEBUG_FORMAT = Fore.RED + "[JARVIS-m-2.0 : Debug] "
DEBUG_STATUS = False
DEBUG_MIC = False # False -> Microphone, True -> Input()

# OPENAI
OPENAI_URL = os.getenv("OPENAI_URL")
