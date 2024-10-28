import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
import json

url = "https://tasks.aidevs.pl/token/tools"
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

tool = {"tool":"ToDo",
        "desc":"Kup mleko" }

calendar = {"tool":"Calendar",
        "desc":"Kup mleko",
        "date": "2024-04-10"  }

chat = ChatOpenAI(temperature=0)

messages = [
SystemMessage(
    content=f"""Decide whether the task should be added to the ToDo list or to the calendar': 
        rules###
        - Todo when is task to do with no deadline
        - Calendar when time is specified. Put date in field date

        In field desc put provided instruction
        if field tool decide its a Calendar or ToDo

        examples ### calendar {{"tool":"Calendar",
        "desc":"Kup mleko",
        "date": "2024-04-10"}}
        
        example ToDo
        tool = {{"tool":"ToDo",
        "desc":"Kup mleko" }}

        ### Tylko json i nic więcej.
        """
),
HumanMessage(
    content=f"{question}"
),
]
answer = chat.invoke(messages).content

print(answer)

parsed_answer = json.loads(answer)
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": parsed_answer
}

response = requests.post(url, json=data)
print(response.text)