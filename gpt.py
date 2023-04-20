import secretkeys
import json
import re
import requests
import datetime
import openai
import time
import webbrowser
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

openai.api_key = secretkeys.openaikey

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output_data = {}
    if request.method == 'POST':
        input_text = request.form['stock']
        output_data = stock_analysis(input_text)
    return render_template('index.html', output_data=output_data)

def article_opinion(stock,article):
    prompt = f"You are an expert financial analyst. Give me your opinion on the performance and outlook of {stock} according to the following text: '{article}'"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=500,
        n=1,
        stop=None,
        timeout=10,
    )
    summary = response.choices[0].text.strip()

    return summary

def opinions_summary(stock,opinions):
    prompt = f"You are an expert financial analyst. Give me your opinion and summary on the performance and outlook of {stock} according to the following opinions that are presented as a JSON string: '{opinions}'. Do not copy the original text from the opinions. You must make an executive summary with a maximum of 5 sentences."
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
        "apiKey" : secretkeys.newskey,
        "category" : "business",
        # "language" : "en"
    }
    url = "https://newsapi.org/v2/top-headlines"
    response = requests.get(url,params=payload).text
    return response

def webscrapper(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find("body")
    text = re.sub("<.*?>", " ", job_elements.text)
    # text = re.sub("<.*?>", " ", soup.prettify())
    text = text.replace('\n','')
    start = ""
    while (start != text):
        start = text
        text = text.replace('  ',' ')
    result = text
    return result


def stock_analysis(stock):
    t = get_today_news(stock)
    a = json.loads(t)

    print(a["totalResults"])

    opinions = []
    urls = []

    for article in a["articles"]:
        URL = article["url"]
        urls.append(URL)
        print(URL)
        article = webscrapper(URL)
        summary = article_opinion(stock,article)
        # print(summary)
        opinions.append(summary)
        time.sleep(3)

    jopinions = json.dumps(opinions)

    final_summary = opinions_summary(stock,jopinions)

    str_urls = ', '.join(urls)

    output_data = {
        "summary" : final_summary,
        "articles": a["totalResults"],
        "urls" : str_urls
    }

    # print(jopinions)
    # print(final_summary)
    return output_data

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False, host='127.0.0.1')
