# importing neccessary module
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