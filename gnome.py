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

url = "https://tasks.aidevs.pl/token/gnome"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
#print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

response_data = response.json()
url = response_data['url']
question = response_data['msg']


from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": question},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

choice = response.choices[0].message.content
#print(input_value)
print(choice)



url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": choice
}

response = requests.post(url, json=data)
print(response.text)