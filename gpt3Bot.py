import openai
import speech_recognition as sr
from gtts import gTTS
import os
import pygame

openai.api_key = "YOUR_API_KEY"

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Você"
bot_name = "BotSexo 0.1"

pygame.init()
pygame.mixer.init()

while True:
    with mic as source:
        print("\nOuvindo...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("Ok...\n")

    try:
        user_input = r.recognize_google(audio, language='pt-BR')
    except:
        continue


    prompt = user_name + ": " + user_input + "\n" + bot_name+ ": "
    conversation += prompt 

    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=100)
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

    conversation += response_str + "\n"
    print(response_str)

    tts = gTTS(text=response_str, lang='pt-br')
    tts.save("response.mp3")
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    os.remove("response.mp3")
