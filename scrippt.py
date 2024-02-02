import datetime
import os
import pyttsx3
import pyautogui
import pyjokes
import pywhatkit
import speech_recognition as sr
import wikipedia
import time as t
import webbrowser
listener = sr.Recognizer()
# to give alexa voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def initial_greeting():
    talk("Hello! I'm ready to assist you.")

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening....")
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'nova' in command:
                command = command.replace('nova', '')
                print(command)
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that. Can you please repeat?")
        return take_command()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return command

def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
        try:
            search_url = f"https://www.youtube.com/results?search_query={song}"
            webbrowser.open(search_url)
        except Exception as e:
            print(f"Error opening the YouTube URL: {e}")
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print(current_time)
        talk('Current time is ' + current_time)
    elif 'search' in command:
        query = command.replace('search', '')
        talk(f'Searching for {query} on Google')
        # Open the browser (you can customize this based on your browser and system)
        pyautogui.hotkey('winleft')
        t.sleep(1)
        pyautogui.write('chrome')  # Replace with your browser's name if not using Chrome
        pyautogui.press('enter')
        t.sleep(2)
        # Type the search query
        pyautogui.write(f'{query} site:google.com')
        pyautogui.press('enter')
    elif 'wikipedia' in command or 'who' in command:
        who = command.replace('wikipedia', '').replace('who', '')
        info = wikipedia.summary(who, 1)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'shutdown' in command:
        talk("Shutting down the computer. Goodbye!")
        os.system("shutdown /s /t 1")
    elif 'open notepad' in command:
        os.system("notepad")
    elif 'close notepad' in command:
        os.system("taskkill /im notepad.exe /f")
    elif 'open image' in command:
        # Replace the path with the location of your image folder
        image_folder_path = r"D:\desktop wallpaper"
        image_files = [f for f in os.listdir(image_folder_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if image_files:
            selected_image = os.path.join(image_folder_path, image_files[0])
            os.startfile(selected_image)
        else:
            talk("No images found in the specified folder.")
    elif 'stop' in command:
        talk("Goodbye!")
        exit()
    else:
        talk("Please say the command again.")

# Initial greeting
initial_greeting()

# Introduce a delay of 30 seconds before starting the main loop
t.sleep(3)

if __name__ == "__main__":
    initial_greeting()
    while True:
        run_alexa()