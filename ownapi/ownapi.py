import requests
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

import logging, ngrok
from flask import Flask, request
from threading import Thread

# Load API keys from the .env file
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
NGROK_AUTH_TOKEN = os.environ.get('NGROK_AUTH_TOKEN')
AI_DEV_TOKEN = os.environ.get('AI_DEV_TOKEN')
token = None
conversation_info = ""

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello"

@app.route('/', methods=['POST'])
def process():
    global token
    global conversation_info
    request_question = request.json['question']
    print(f'Question: {request_question}')
    chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

    decision = chat.invoke(
        [
            SystemMessage(
                content='''Decide it's a question or information. Respond in one word. Only question or information word are available.'''
            ),
            HumanMessage(
                content=request_question
            )
        ]
    )
    if decision.content.lower() == 'information':
        conversation_info += conversation_info + request_question

    answer = chat.invoke(
        [
            SystemMessage(
                content=f'''Respond to message. If user propmt is question answer to the given question consciously as possible. Use only one or two words if possible.
                If it's not question respond to message.
                Remember information from responder about him/her {conversation_info}. Use this info in converasation.'''
            ),
            HumanMessage(
                content=request_question
            )
        ]
    )
    print(f'Chat answer: {answer.content}')
    answer = { 'reply': answer.content }

    url = f"https://tasks.aidevs.pl/answer/{token}"

    response = requests.post(url, json=answer)
    print(response)
    return answer

def run_server():
    app.run()

def main():
    global token
    # Configure Ngrok
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    logging.basicConfig(level=logging.INFO)
    listener = ngrok.werkzeug_develop()

    # In new thread start flask server
    t = Thread(target=run_server)
    t.start()

    url = "https://tasks.aidevs.pl/token/ownapipro"
    data = {
        "apikey": AI_DEV_TOKEN
    }

    response = requests.post(url, json=data)
    token = response.json()['token']
    print(token)
    #print(response.json())

    response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
    print(response.text)

    answer = {
        'answer': listener.url()
    }

    url = f"https://tasks.aidevs.pl/answer/{token}"

    response = requests.post(url, json=answer)
    print(response.text)


if __name__ == "__main__":
    main()