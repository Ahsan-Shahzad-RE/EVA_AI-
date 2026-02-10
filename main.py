# Eva AI Assistant

import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv


load_dotenv()
MY_OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
MY_NEWS_KEY = os.environ.get("NEWS_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()

    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiprocess(command):
    client = OpenAI(api_key=MY_OPENAI_KEY)
    completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role" : "system" , "content" : "You are a virtual assistant named Eva skilled in general tasks like Alexa and google.Give short responses please"},
        {"role" : "user" , "content" : command}
        
    ]
    )
    return completion.choices[0].message.content


#these are features we can add to Zoe
def processcommand(c):
    
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif  "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif  "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        # song = c.lower().split(" ")[1]
        song = c.lower().replace("play" , "").strip()
        print(f"DEBUG: Trying to find the song key: '{song}'")
        try :
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        except KeyError:
            print(f"ERROR : Song Key '{song}' not found ")
            speak(f"sorry, I can't find {song} in your Library")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={MY_NEWS_KEY}")
        


        if r.status_code == 200:
            #parse the JSON response
            data = r.json()
            #extract the news articles
            articles = data.get("articles" , [])
            for article in articles:
                speak(article["title"])

    else:
        # let openai handle the requests
        output = aiprocess(c)
        speak(output)
        pass



if __name__ == "__main__":
    speak("Hello! I am Eva, Call my name , I will assist you.")
    while True:
        r = sr.Recognizer()

        print("Recognizing....")
        try :
            with sr.Microphone() as source:
                print("Calibrating for ambient noise...")
                r.adjust_for_ambient_noise(source , duration=1) #added feature
                print("listening for wake word...")
                audio = r.listen(source , timeout=10)
            word = r.recognize_google(audio , language = "en-US")
            print(f"I heard: {word}")
            
            
            if (word.lower() == "eva"):
                speak("Yeah...?")
                #listen for command
                with sr.Microphone() as source:
                    print("Eva is Active... Calibrating...")
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio , language = "en-US")

                    processcommand(command)

        except Exception as e :
            print("error ; {0}".format(e))






# import asyncio

# async def main():
#     print('Hello ...')
#     await asyncio.sleep(1)
#     print('... World!')
# asyncio.run(main())


