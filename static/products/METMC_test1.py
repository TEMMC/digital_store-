import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser

# =========================
# VOICE ENGINE (TEXT TO SPEECH)
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("METMC:", text)
    engine.say(text)
    engine.runAndWait()

# =========================
# LISTENER (VOICE INPUT)
# =========================
listener = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except:
        return "none"

# =========================
# CORE BRAIN
# =========================
def brain(command):

    if "time" in command:
        return "Current time is " + datetime.datetime.now().strftime("%H:%M:%S")

    if "date" in command:
        return "Today is " + datetime.datetime.now().strftime("%Y-%m-%d")

    if "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "cpu" in command:
        return "CPU monitoring not enabled in voice mode yet"

    if "hello" in command:
        return "Hello. METMC voice system online."

    if "your name" in command:
        return "I am METMC, your voice AI assistant."

    if "exit" in command or "stop" in command:
        return "shutdown"

    return "I did not understand that command"

# =========================
# STARTUP
# =========================
speak("METMC voice system activated")

# =========================
# MAIN LOOP
# =========================
while True:
    command = listen()

    if command == "none":
        continue

    response = brain(command)

    if response == "shutdown":
        speak("Shutting down METMC.")
        break

    speak(response)