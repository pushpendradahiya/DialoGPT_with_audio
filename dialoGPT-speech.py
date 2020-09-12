import speech_recognition as sr
import pyttsx3
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch

WIT_AI_KEY = "ZMGF2KUHBDEWY4Y35HLFB3IIK75LPZQC"
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-medium")

engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 0.9)
r = sr.Recognizer()


speech = sr.Microphone(device_index=1)
print("System Ready, Speak Something")
for step in range(5):
    print("You: ",end="")
    with speech as source: 
        audio = r.adjust_for_ambient_noise(source) 
        audio = r.listen(source)
    try:    
        recog = r.recognize_wit(audio, key = WIT_AI_KEY)
        # recog = r.recognize_google(audio)    
        print(recog) 
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(recog + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        chat_out = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("BOT: {}".format(chat_out))   
        engine.say(chat_out)    
        engine.runAndWait()
    except sr.UnknownValueError:    
        engine.say("Google Speech Recognition could not understand audio")    
        engine.runAndWait()
    except sr.RequestError as e:    
        engine.say("Could not request results from Google Speech Recognition service; {0}".format(e))    
        engine.runAndWait()