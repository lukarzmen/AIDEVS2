import json
import uuid
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

url = "https://unknow.news/archiwum_aidevs.json"

response = requests.get(url)
data = response.json()

parsed_data = [] 
for item in data: 
    title = item.get("title", "") 
    url = item.get("url", "") 
    info = item.get("info", "") 
    parsed_data.append({"title": title, "url": url, "info": info})


url = "https://tasks.aidevs.pl/token/search"
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

import chromadb
client = chromadb.EphemeralClient()
collection = client.create_collection("sample_collection")
client.clear_system_cache()

# Add docs to the collection. Can also update and delete. Row-based API coming soon!
collection.add(
    documents=[str(item) for item in parsed_data], 
    ids=[str(uuid.uuid1()) for _ in parsed_data]
)

results = collection.query(
    query_texts=[question],
    n_results=3,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
) 

chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content=f"Odpowiedz na pytanie posiadając kontekst ### Pojęcia „pseudonimizacja” i „anonimizacja” są ważnymi elementami procesów ochrony danych. Odnosi się do nich bezpośrednio treść RODO i powołują się na nie podmioty przetwarzające dane, gdy bronią się przed UODO w trakcie postępowania wszczętego na podstawie naszej skargi. Co jednak dokładnie znaczą te słowa? W tej rozmowie adwokatka Agnieszka Rapcewicz i kryptolog dr inż. Michał Ren podejmują próbę pogodzenia prawnych i matematycznych definicji tych pojęć. ###"
),
HumanMessage(
    content=f"{question}"
),
]
result = chat.invoke(messages).content

print(results)


url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": "https://www.internet-czas-dzialac.pl/pseudonimizacja-a-anonimizacja/"
}

response = requests.post(url, json=data)
print(response.text)

