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

url = "https://tasks.aidevs.pl/token/inprompt"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
#print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
#print(response.text)

response_data = response.json()
data = response_data['input']
question = response_data['question']

#print(input_value)
print(question)

knowledge_base = [element for element in data if "Ezaw" in element]
print(knowledge_base)

chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content=f"Odpowiadaj na pytania. Posiadając kontekst ### {data} ###"
),
HumanMessage(
    content=f"{question}"
),
]
result = chat.invoke(messages).content

print(result)

url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": result
}

response = requests.post(url, json=data)
print(response.text)
