from dotenv import load_dotenv
import requests
from langchain_core.messages import HumanMessage, SystemMessage
import openai
from langchain_openai import ChatOpenAI

load_dotenv()

url = "https://tasks.aidevs.pl/token/embedding"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
#print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

import openai
embedding = openai.embeddings.create(
  input="Hawaiian pizza",
  model="text-embedding-ada-002",
  encoding_format="float"
)


# Extract the embedding array
embedding_array = embedding.data[0].embedding


url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": embedding_array
}

response = requests.post(url, json=data)
print(response.text)