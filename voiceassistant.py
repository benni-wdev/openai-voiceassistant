import os
# environment variables from .env file
import dotenv
# proper log messages as output
import logging
# speech to text module
import speech_recognition as sr
# text to speech module
import pyttsx3
# openai api module to ask chatgpt
import openai

# ----------- configure and init modules -----------
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO
)
dotenv.load_dotenv()
r = sr.Recognizer()
# configure used openai model
openai_model = "gpt-3.5-turbo"
# openai api key should be stored in .env file next to this file with OPENAI_API_KEY=the-key
openai.api_key = os.getenv('OPENAI_API_KEY')
engine = pyttsx3.init()
# ----------- configure voice assistant -----------
# activation name (small letters)
assistant_name = "alberto"
# timeout in seconds when no noise
timeout_listen_per_round = 10
# minimal seconds listened on input (name must fit)
min_timeout_listen_on_voice = 5
# dynamic seconds listened on input (x listeningMode)
max_timeout_factor_listen_on_voice = 5
# when 1 no openai api call instead a fix text is returned
test_mode = 0
# key word to bring running assistant into test mode
test_mode_keyword = "testmodus"
# the fixed message for test mode
test_message = "Das ist nur eine Testausgabe"

# ----------- Language config -----------
# output speech - language
engine.setProperty("voice", "german")
# input speech - language
speech_to_text_lang = "de-DE"
# Message when activated by name
confirm_listening_text = "Ja ich höre"
# assistant_name + this string signals stop listening
end_keyword = " ende"
# Message when deactivated
confirm_stop_text = "Es war mir eine Ehre zu dienen"
# Trigger long question mode
long_input_keyword = "lange frage"
# Message when long question mode activated
confirm_long_input_text = "OK ich höre dir länger zu"
# Trigger program exit
program_exit_keyword = "beende dich"
# Message when long question mode activated
confirm_program_exit_text = "Lebe lang und in Frieden"


# Function to convert text to speech
def speak_text(command):
    engine.say(command)
    engine.runAndWait()


# Function for invoking openai model
def get_openai_response(prompt):
    if test_mode == 1:
        return test_message
    else:
        completion = openai.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return completion.choices[0].message.content


logging.info("Voice Assistant is listening...")
listening_mode = 0
running = True
while running:
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source_mic:
            # adjust the energy threshold based on
            # the surrounding noise level
            logging.info("adjust noise")
            r.adjust_for_ambient_noise(source_mic, duration=0.2)
            # listens for the user's input
            logging.info("Listening in mode " + str(listening_mode))
            captured_audio = r.listen(
                source_mic,
                timeout_listen_per_round,
                listening_mode * max_timeout_factor_listen_on_voice + min_timeout_listen_on_voice
            )
            logging.info("audio captured")
            # Using google to recognize audio
            user_input = r.recognize_google(captured_audio, language=speech_to_text_lang)
            logging.info("Captured text:" + user_input)
            if listening_mode == 0:
                if user_input.lower() in [assistant_name]:
                    logging.info("Voice Assistant activated")
                    speak_text(confirm_listening_text)
                    listening_mode = 1
                    test_mode = 0
            else:
                if user_input.lower() in [assistant_name + end_keyword]:
                    logging.info("Voice Assistant sleeps...")
                    speak_text(confirm_stop_text)
                    listening_mode = 0

                elif user_input.lower() in [program_exit_keyword]:
                    logging.info("Voice Assistant exiting...")
                    speak_text(confirm_program_exit_text)
                    running = False

                elif user_input.lower() in [long_input_keyword]:
                    logging.info("Voice Assistant extending input length")
                    speak_text(confirm_long_input_text)
                    listening_mode = 3

                elif user_input.lower() in [test_mode_keyword]:
                    logging.info("Voice Assistant going to test mode")
                    speak_text(test_mode_keyword)
                    test_mode = 1

                else:
                    logging.info("Asking " + openai_model)
                    openaiResponse = get_openai_response(user_input)
                    logging.info("text to speech:" + openaiResponse)
                    speak_text(openaiResponse)

    except sr.RequestError as e:
        logging.error("Could not request results; {0}".format(e))

    except sr.UnknownValueError as e:
        logging.error("unknown error: {0}".format(e))
