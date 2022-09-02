import secrets
import json
import requests
import datetime
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    ta_credential = AzureKeyCredential(secrets.key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=secrets.endpoint, 
            credential=ta_credential)
    return text_analytics_client

def sentiment_analysis_with_opinion_mining(client,documents):

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
    negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

    positive_mined_opinions = []
    mixed_mined_opinions = []
    negative_mined_opinions = []

    for document in doc_result:
        print("Document Sentiment: {}".format(document.sentiment))
        print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f}".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        ))
        print("\n")

def get_today_news(query):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    payload = {"q":query,"from":today,"sortBy":"published","apiKey":secrets.newskey}
    url = "https://newsapi.org/v2/everything"
    response = requests.get(url,params=payload)
    return response

client = authenticate_client()

filename = "demo.json"
f = open(filename,"r")
t = f.read()

# t = get_today_news("ether")

a = json.loads(t)
r = []
batch_limit = 10

for article in a["articles"]:
    r.append(article["description"])
    if len(r) == batch_limit:
        sentiment_analysis_with_opinion_mining(client,r)
        r = []
