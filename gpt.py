import secrets
import json
import re
import requests
import datetime
import openai
import time
from bs4 import BeautifulSoup

openai.api_key = secrets.openaikey

def article_opinion(stock,article):
    prompt = f"You are an expert financial analyst. Give me your opinion on the performance and outlook of {stock} according to the following text: '{article}'"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        n=1,
        stop=None,
        timeout=10,
    )
    summary = response.choices[0].text.strip()

    return summary

def opinions_summary(stock,opinions):
    prompt = f"You are an expert financial analyst. Give me your opinion and summary on the performance and outlook of {stock} according to the following opinions that are presented as a JSON string: '{opinions}'. Do not copy the original text from the opinions. You must make an executive summary."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        n=1,
        stop=None,
        timeout=10,
    )
    summary = response.choices[0].text.strip()

    return summary

def get_today_news(query):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    payload = {
        "q"      : query,
        "from"   : today,
        "sortBy" : "published",
        "apiKey" : secrets.newskey,
        "category" : "business",
        # "language" : "en"
    }
    url = "https://newsapi.org/v2/top-headlines"
    response = requests.get(url,params=payload).text
    return response

def webscrapper(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find("article")
    result = re.sub("<.*?>", " ", job_elements.text)
    return result

stock = "Alibaba"

t = get_today_news(stock)
a = json.loads(t)

print(a["totalResults"])

opinions = []

for article in a["articles"]:
    URL = article["url"]
    # print(URL)
    article = webscrapper(URL)
    summary = article_opinion(stock,article)
    # print(summary)
    opinions.append(summary)
    time.sleep(3)

jopinions = json.dumps(opinions)

final_summary = opinions_summary(stock,jopinions)

print(jopinions)
print(final_summary)