# importing neccessary module
from time import sleep
import os
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = "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"
import pyttsx3
import speech_recognition as sr #pip install speechrecognition

# Listening commands by speach recognition module
def Listen():
    r = sr.Recognizer()

    # accessing microphone
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)  # Listening Mode.....

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en")

    except:
        return ""

    query = str(query).lower()
    print("You: " + query)
    return query


# Function Speaking
def Speak(Text):
    # Selecting default voice
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[1].id)
    engine.setProperty('rate',170)
    print("")
    print(f"AI : {Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()

# Accessing OpenAi API
client = OpenAI()

starting_assistant = ""
starting_thread = ""


def create_assistant():
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            # Giving costume instruction
            instructions="You are windows voice assistant that can help people any way",
            name="Smeet",
            model="gpt-3.5-turbo",
        )
    else:
        my_assistant = client.beta.assistants.retrieve(starting_assistant)

    return my_assistant


def create_thread():
    if starting_thread == "":
        thread = client.beta.threads.create()
    else:
        thread = client.beta.threads.retrieve(starting_thread)

    return thread


def send_message(thread_id, message):
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message


def run_assistant(thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run


def get_newest_message(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data[0]


def get_run_status(thread_id, run_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status

def main():
    my_assistant = create_assistant()
    my_thread = create_thread()

    while True:
        user_message = Listen()
        if user_message.lower() == "exit":
            break

        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)
        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)
            sleep(1)
            print("⏳", end="\r", flush=True)

        response = get_newest_message(my_thread.id)
        # print("Response:", response.content[0].text.value)
        Speak(response.content[0].text.value)

if __name__ == "__main__":
    main()
