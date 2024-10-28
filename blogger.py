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

url = "https://tasks.aidevs.pl/token/blogger"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

topics = response.json()['blog']
chat = ChatOpenAI(temperature=0)

blog = []

for topic in topics:
    messages = [
    SystemMessage(
        content="Jesteś twórcą bloga. Napisz artykuł bloga na temat: "
    ),
    HumanMessage(
        content=f"{topic}"
    ),
    ]
    chapter = chat.invoke(messages).content
    print(chapter)
    blog.append(chapter)

answer = ""
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": blog
}

response = requests.post(url, json=data)
print(response.text)