import random
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
import time
# Retry with backoff policy
def get_response_with_backoff(url):
    max_retries = 20
    retry_delay = 1

    for i in range(max_retries):
        retry_delay = random.randint(1, 10)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                time.sleep(retry_delay)
                
                continue
            return response
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise
def ask_chatbot(response, question):
    chat = ChatOpenAI(temperature=0)

    messages = [
SystemMessage(
    content=f"""Odpowiedz na pytanie na podstawie dostarczonego kontekstu. 
    Kontekst: ### The first concrete information on pasta products in Italy dates to the 13th or 14th centuries.
In the 1st century AD writings of Horace, lagana (singular: laganum) were fine sheets of fried dough and were an everyday foodstuff. Writing in the 2nd century, Athenaeus of Naucratis provides a recipe for lagana which he attributes to the 1st century Chrysippus of Tyana: sheets of dough made of wheat flour and the juice of crushed lettuce, then flavoured with spices and deep-fried in oil. An early 5th century cookbook describes a dish called lagana that consisted of layers of dough with meat stuffing, an ancestor of modern-day lasagna. However, the method of cooking these sheets of dough does not correspond to the modern definition of either a fresh or dry pasta product, which only had similar basic ingredients and perhaps the shape. The first concrete information concerning pasta products in Italy dates from the 13th or 14th century.Historians have noted several lexical milestones relevant to pasta, none of which changes these basic characteristics. For example, the works of the 2nd century AD Greek physician Galen mention itrion, homogeneous compounds made of flour and water. The Jerusalem Talmud records that itrium, a kind of boiled dough, was common in Palestine from the 3rd to 5th centuries AD. A dictionary compiled by the 9th century Arab physician and lexicographer Isho bar Ali defines itriyya, the Arabic cognate, as string-like shapes made of semolina and dried before cooking. The geographical text of Muhammad al-Idrisi, compiled for the Norman King of Sicily Roger II in 1154 mentions itriyya manufactured and exported from Norman Sicily:

West of Termini there is a delightful settlement called Trabia [along the Sicilian coast east of Palermo]. Its ever-flowing streams propel a number of mills. Here there are huge buildings in the countryside where they make vast quantities of itriyya which is exported everywhere: to Calabria, to Muslim and Christian countries. Very many shiploads are sent.
One form of itriyya with a long history is lagana, which in Latin refers to thin sheets of dough, and gave rise to the Italian lasagna.

In North Africa, a food similar to pasta, known as couscous, has been eaten for centuries. However, it lacks the distinguishing malleable nature of pasta, couscous being more akin to droplets of dough. At first, dry pasta was a luxury item in Italy because of high labor costs; durum wheat semolina had to be kneaded for a long time.
There is a legend of Marco Polo importing pasta from China which originated with the Macaroni Journal, published by an association of food industries with the goal of promoting pasta in the United States. Rustichello da Pisa writes in his Travels that Marco Polo described a food similar to "lagana". Jeffrey Steingarten asserts that Arabs introduced pasta in the Emirate of Sicily in the ninth century, mentioning also that traces of pasta have been found in ancient Greece and that Jane Grigson believed the Marco Polo story to have originated in the 1920s or 1930s in an advertisement for a Canadian spaghetti company.Food historians estimate that the dish probably took hold in Italy as a result of extensive Mediterranean trading in the Middle Ages. From the 13th century, references to pasta dishes—macaroni, ravioli, gnocchi, vermicelli—crop up with increasing frequency across the Italian peninsula. In the 14th-century writer Boccaccio's collection of earthy tales, The Decameron, he recounts a mouthwatering fantasy concerning a mountain of Parmesan cheese down which pasta chefs roll macaroni and ravioli to gluttons waiting below.In the 14th and 15th centuries, dried pasta became popular for its easy storage. This allowed people to store pasta on ships when exploring the New World. A century later, pasta was present around the globe during the voyages of discovery.Although tomatoes were introduced to Italy in the 16th century and incorporated in Italian cuisine in the 17th century, description of the first Italian tomato sauces dates from the late 18th century: the first written record of pasta with tomato sauce can be found in the 1790 cookbook L'Apicio Moderno by Roman chef Francesco Leonardi. Before tomato sauce was introduced, pasta was eaten dry with the fingers; the liquid sauce demanded the use of a fork. ###. 
    Jeśli w kontekcie nie ma dostarczonej informacji odpowiedz zwrotem "Nie wiem".
    Nie zmyślaj.
    """
),
HumanMessage(
    content=f"{question}"
),
]
    result = chat.invoke(messages).content

    print(result)
    return result

url = "https://tasks.aidevs.pl/token/scraper"
data = {
    "apikey": ""
}

response = requests.post(url, json=data)
token = response.json()['token']
print(token)
print(response.json())



# Call the function with the input_text_url
# def qa(get_response_with_backoff, ask_chatbot, token):
#     response = get_response_with_backoff(f"https://tasks.aidevs.pl/task/{token}")
#     print(response.text)

    
#     responser = response.json()
#     input_text_url = responser['input']
#     question = responser['question']

#     response = get_response_with_backoff(input_text_url)
#     if response is None:
#         return
#     print(response.text)
#     if response.text == "bot detected!" or response.text == "server error X_X":
#         return
#     result = ask_chatbot(response, question)
#     return result

#result = qa(get_response_with_backoff, ask_chatbot, token)

# while result != "Nie wiem":
#     result = qa(get_response_with_backoff, ask_chatbot, token)
#     time.sleep(5)

    
response = get_response_with_backoff(f"https://tasks.aidevs.pl/task/{token}")
print(response.text)

    
responser = response.json()
input_text_url = responser['input']
question = responser['question']
result = ask_chatbot(response, question)
url = f"https://tasks.aidevs.pl/answer/{token}"
data = {
    "answer": result
}

response = requests.post(url, json=data)
print(response.text)