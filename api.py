import requests

url = "https://tasks.aidevs.pl/token/helloapi"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

cookie = response.json()['cookie']
print(cookie)

answer = "tutaj wpisujesz odpowiedz"
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": cookie
}

response = requests.post(url, json=data)
print(response.text)