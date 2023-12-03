# openai-voiceassistant
A simple voice assistant with speech input and output based on openai api (chatgpt).
It features:
  - voice controlled: only listens on configurable keyword (assistant_name)
  - voice controlled: exits listening mode on keyword
  - voice controlled: enters test mode on keyword (no openai api call, just dummy text)
  - voice controlled: can extend listening timeout on command
## Prerequisites
Scripts expects an environment variable called OPENAI_API_KEY with an active api key to execute the api call.
It can be specified in a .env file next to main script (script would fetch it automatically).

Needed python modules:
  - pyaudio
  - dotenv
  - logging
  - speech_recognition
  - pyttsx3
  - openai

## configurations
Multiple configurations are possible at the beginning of the script:
  - language (configured german)
  - keywords and confirm messages
  - timeouts
  - used openai model

More informations can be found here: https://www.wdev.ch/how-to-create-your-own-voice-assistant-with-python-and-chatgpt-api/
