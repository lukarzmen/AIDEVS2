import uuid
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from qdrant_client.http.models import Record

url = "https://tasks.aidevs.pl/token/people"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

question = response.json()['question']


chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content=f"Co w tekście jest imieniem i nazwiskiem. Tylko imię i nazwisko i nic więcej."
),
HumanMessage(
    content=f"{question}"
),
]
answer = chat.invoke(messages).content

print(answer)


url = response.json()['data']

print(url)
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer('all-MiniLM-L6-v2')

data_response = requests.get(url)
data = data_response.json()
data_array = []
for item in data:
    # Extracting the required information from the data dictionary
    imie = item['imie']
    nazwisko = item['nazwisko']
    wiek = item['wiek']
    o_mnie = item['o_mnie']
    ulubiona_postac_z_kapitana_bomby = item['ulubiona_postac_z_kapitana_bomby']
    ulubiony_serial = item['ulubiony_serial']
    ulubiony_film = item['ulubiony_film']
    ulubiony_kolor = item['ulubiony_kolor']

    # Concatenate all the data to one string
    data_string = f"{imie} {nazwisko} wiek {wiek} {o_mnie} ulubiona postać z kapitana bomby to  {ulubiona_postac_z_kapitana_bomby} ulubiony serial {ulubiony_serial} ulubiony film {ulubiony_film} ulubiony kolor {ulubiony_kolor}"
    data_array.append(data_string)

from qdrant_client import QdrantClient
qdrant = QdrantClient(":memory:")


records = [Record(id=i, payload={"text": string}) for i, string in enumerate(data_array)]
ids = list(map(lambda record: record.id, records))
qdrant.add(
    collection_name="qa",
    documents=data_array,
    ids=ids
)

hits = qdrant.query(
    collection_name="qa",
    query_text=answer,
    limit=5
)
for hit in hits:
  print(hit.document, "score:", hit.score)

chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content=f"Odpowiedz na pytanie na podstawie dostarczonego kontekstu: ###{hits[0].document}"
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



