from imp import load_module

from dotenv import load_dotenv
import requests
from langchain_core.messages import HumanMessage, SystemMessage
import openai
from langchain_openai import ChatOpenAI
import whisper
import wget
import whisper


load_dotenv()

url = "https://tasks.aidevs.pl/token/whisper"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
#print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

model = whisper.load_model('base')
import urllib.request

file_url = "https://tasks.aidevs.pl/data/mateusz.mp3"
# wget.download(file_url)

result = model.transcribe("mateusz.mp3")
transcription = result["text"]
transcription = transcription.strip()
transcription = transcription.replace("szurcznej", "sztucznej")



url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": transcription
}

response = requests.post(url, json=data)
print(response.text)