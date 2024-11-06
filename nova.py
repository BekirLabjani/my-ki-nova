import os
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import time
from pywinauto import Application
import psutil

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=10)
        except Exception as e:
            print("Error accessing microphone:", e)
            return 'none'
    try:
        print('Recording...')
        query = r.recognize_google(audio, language='de-DE')
        print(f'User said: {query}')
        return query
    except Exception as e:
        speak('Say that again.')
        return 'none'


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak('Good morning!')
    elif hour < 18:
        speak('Good day!')
    else:
        speak('Good evening!')
    speak("I am Nova, your personal assistant. How can I help you?")


def is_spotify_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Spotify.exe':
            return True
    return False


def start_spotify():
    spotify_path = "C:\\Users\\Bekir\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"  # Change this path if necessary
    os.startfile(spotify_path)
    speak("Starting Spotify.")


def play_music():
    try:
        app = Application().connect(process='Spotify.exe')  # Connect to Spotify by process name
        app.Spotify.set_focus()  # Focus on the Spotify window
        time.sleep(1)  # Wait for the window to focus

        # Print control identifiers to see available elements (useful for identifying Play button)
        app.Spotify.print_control_identifiers()

        # Try to click the Play button
        app.Spotify.child_window(title="Play",
                                 control_type="Button").click()  # Adjust based on control identifier from print_control_identifiers
        speak("Playing your music.")
    except Exception as e:
        speak("Could not connect to Spotify. Please make sure it is open.")
        print(e)  # Print the error for debugging


def put_pc_in_sleep():
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Windows command to put PC in sleep mode
        speak("Putting the computer to sleep now.")
    except Exception as e:
        speak("There was an error while putting the computer to sleep.")
        print(e)


if __name__ == '__main__':
    wish()
    while True:
        query = takeCommand().lower()
        if "stop" in query:
            print("Ending the assistant.")
            break

        elif any(command in query for command in ["open web", 'chrome open', 'start chrome']):
            npath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(npath)
            print("Opening the web browser.")

        elif any(command in query for command in ["youtube", "open youtube", "tube"]):
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")

        elif any(command in query for command in ["spotify", "start spotify"]):
            if not is_spotify_running():
                start_spotify()
            else:
                speak("Spotify is already running.")

        elif "play music" in query:
            if is_spotify_running():
                play_music()
            else:
                speak("Spotify is not running.")
                print("Spotify is not running.")

        elif "sleep my pc" in query:
            put_pc_in_sleep()  # Put PC in sleep mode
