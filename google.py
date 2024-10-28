import time
from dotenv import load_dotenv
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

load_dotenv()

url = "https://tasks.aidevs.pl/token/google"
data = {
    "apikey": ""
}

fetch_data_response = requests.post(url, json=data)
token = fetch_data_response.json()['token']
print(token)
print(fetch_data_response.json())

fetch_data_response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(fetch_data_response.text)
response_json = fetch_data_response.json()


zygfryd = shorten_info(data, "zygfryd")
stefan = shorten_info(data, "stefan")
ania = shorten_info(data, "ania")
    

url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": f"{zygfryd} {ania} {stefan}"
}

fetch_data_response = requests.post(url, json=data)
print(fetch_data_response.text)

