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

url = "https://tasks.aidevs.pl/token/whoami"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

def ask_chatbot(token, hint):
    response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
    print(response.text)
    response_json = response.json()
    hint = response_json['hint']
    print(hint)
    chat = ChatOpenAI(temperature=0)
    messages = [
SystemMessage(
    content="Na podstawie podanego w zapytaniu tekstu odpowaidaj kim mowa? Odpowiadaj ściśle. Tylko imię i nazwisko osoby. Jeśli nie wiesz odpowiedz NIE WIEM."
),
HumanMessage(
    content=f"{hint}"
),
]
    result = chat.invoke(messages).content

    print(result)
    return result, hint

result, hint = ask_chatbot(token, "")
while result == "NIE WIEM." or "Barack Obama" in result or "George Washington" in result or "Jack Kerouac" in result:
    result, hint_new = ask_chatbot(token, hint)
    hint = hint + " " + hint_new
    time.sleep(2)
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": result
}

response = requests.post(url, json=data)
print(response.text)

