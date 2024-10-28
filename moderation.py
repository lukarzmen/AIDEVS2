import requests

url = "https://tasks.aidevs.pl/token/moderation"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

input = response.json()['input']
flagged_values = []

for item in input:
    response = requests.post("https://api.openai.com/v1/moderations",
                             headers={"Content-Type": "application/json",
                                      "Authorization": "Bearer xxxxxxxxxxx"},
                             json={"input": item})
    
    flagged = int(response.json()['results'][0]['flagged'])
    
    flagged_values.append(flagged)
    
    print(response.text)

print(flagged_values)

answer = flagged_values
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": answer
}

response = requests.post(url, json=data)
print(response.text)