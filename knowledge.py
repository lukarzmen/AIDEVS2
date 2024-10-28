import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

url = "https://tasks.aidevs.pl/token/knowledge"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

question = response.json().get("question", "")
print(question)

context1 = requests.get("http://api.nbp.pl/api/exchangerates/tables/A")
print(context1.text)

chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content=f"Odpowiedz na pytanie na podstawie dostarczonego kontekstu: ###{context1.text} ### Podaj tylko wartość liczbową. Bez formatowania."
),
HumanMessage(
    content=f"{question}"
),
]
answer = chat.invoke(messages).content

url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": answer
}

response = requests.post(url, json=data)
print(response.text)
# response = requests.get("https://restcountries.com/")
# print(response.text)

