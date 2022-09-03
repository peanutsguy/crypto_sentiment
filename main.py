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

    pos = []
    neu = []
    neg = []

    for document in doc_result:
        pos.append(document.confidence_scores.positive)
        neu.append(document.confidence_scores.neutral)
        neg.append(document.confidence_scores.negative)
    
    return [sum(pos)/len(pos),sum(neu)/len(neu),sum(neg)/len(neg)]

def get_today_news(query):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    payload = {
        "q"      : query,
        "from"   : today,
        "sortBy" : "published",
        "apiKey" : secrets.newskey
    }
    url = "https://newsapi.org/v2/everything"
    response = requests.get(url,params=payload)
    return response

client = authenticate_client()

t = get_today_news("ethereum").text

a = json.loads(t)
r = []
batch_limit = 10
scores = {
    "positive": [],
    "neutral" : [],
    "negative": []
}

for article in a["articles"]:
    r.append(article["description"])
    if len(r) == batch_limit:
        sentiment = sentiment_analysis_with_opinion_mining(client,r)
        r = []
        scores["positive"].append(sentiment[0])
        scores["neutral"].append(sentiment[1])
        scores["negative"].append(sentiment[2])

scores["average"] = {
    "positive" : round(sum(scores["positive"])/len(scores["positive"]),3),
    "neutral" : round(sum(scores["neutral"])/len(scores["neutral"]),3),
    "negative" : round(sum(scores["negative"])/len(scores["negative"]),3)
}

print(scores["average"])