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

url = "https://tasks.aidevs.pl/token/liar"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

chat = ChatOpenAI(temperature=0)

question = "What is the biggest city of Poland?"

response = requests.post(f"https://tasks.aidevs.pl/task/{token}", dict(question=question))
print(response.text)
answer = response.json()["answer"]
print(answer)

chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content="Your role is to decide that text specified in prompt is a response to question. Question: {question}. Respond in one word YES or NO."
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

