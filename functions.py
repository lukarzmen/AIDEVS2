import requests
import json

url = "https://tasks.aidevs.pl/token/functions"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())

response = requests.get(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

func = """
{
  "answer": {
    "name": "addUser",
    "description": "Adds a user with their name, surname, and year of birth",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The first name of the user"
        },
        "surname": {
          "type": "string",
          "description": "The surname of the user"
        },
        "year": {
          "type": "integer",
          "description": "The year of birth of the user"
        }
      }
    }
  }
}
"""
func_obj = json.loads(func)
print(func_obj)
url = f"https://tasks.aidevs.pl/answer/{token}"

response = requests.post(url, json=func_obj)
print(response.text)

