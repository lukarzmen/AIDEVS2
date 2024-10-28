import os
import time
import requests

url = "https://tasks.aidevs.pl/token/meme"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

image = response.json()['image']
text = response.json()['text']

print(image)
print(text)

def prepareMeme(image: str, text: str) -> str:
    return requests.post(
        url='https://get.renderform.io/api/v2/render',
        headers={
            'Content-Type': 'application/json',
            'X-API-KEY': os.getenv('RENDERFORM_API_KEY')
        },
        json = {
            'template': "cold-oysters-scrub-softly-1176",
            'data': {
                'image.src': image,
                'title.text': text
            }
        }
    ).json()['href']

memeUrl = prepareMeme(image, text)
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": memeUrl
}

response = requests.post(url, json=data)
print(response.text)

