import google.generativeai as gai
from dotenv import load_dotenv
import os
import tempfile
import pygame
from gtts import gTTS
import pyttsx3
import speech_recognition as sr


# load environment variables
load_dotenv()

#define google api_key in environment variables
gai.configure(api_key=os.environ["Google_API_KEY"])


# define model
model = gai.GenerativeModel('gemini-pro')
#define chat condition
chat = model.start_chat()

#chats with gemini generative ai setting the prompt
def chat_lm(prompt):
    response = model.generate_content(
        contents=prompt,

        stop=None,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    model.generate_content(prompt, stop=None, callbacks=None)


#speaks the text using gtts
def speak(text):
    tts = gTTS(text=text, lang='en')
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    tts.save(temp.name)  # Corrected line

    #pygame setting to record to tempfile and play voice input
    pygame.mixer.init()
    pygame.mixer.music.load(temp.name)
    pygame.mixer.music.play()
    print(text)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()


#define input microphone and speech recognition
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        text = ''
    try:
        text = r.recognize_google(audio)


    #error handling
    except sr.RequestError as re:
        print(re)
        print("Sorry, I encountered an error. Please try again.")
    except sr.UnknownValueError as uve:
        print(uve)
        print("Sorry, I couldn't understand. Please try again.")
    except sr.WaitTimeoutError as wte:
        print(wte)
        print("Sorry, the operation timed out. Please try again.")
    text = text.lower()
    return text


#main loop
if __name__ == "__main__":
    while True:
        human_input = listen()# define human input equal audio source
        prompt=human_input #define prompt equals human input
        print(prompt)#print input
        speak( "User said: " + human_input)# voice playback input

        #error handling if human_input is not defined, then continue loop
        if not human_input:
            print("I didn't catch that. Could you please repeat?")
            speak("I didn't catch that. Could you please repeat?")
            continue
        
        #if human_input is in quit, exit, stop, bye, goodbye, then break loop
        if human_input.lower() in [ "quit", "exit", "stop", "bye", "goodbye"]:
            break

        #define response equal to model.generate_content(human_input)
        response = model.generate_content(human_input)
        #define response_text equal to response.text
        response_text = response.text

        #print text response
        print(response_text)
        #speak text response
        speak(response_text)
