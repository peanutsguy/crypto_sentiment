> Work in progress
>
> At the moment, to avoid excessive API request to newsapi.org, I'm using a JSON file (`demo.json`) I saved from a query I ran on "ether".

This script helps evaluate the average sentiment of news headlines. I'll be orienting it towards crypto sentiment in order to determine if I should buy, sell or hodl.

Based on Microsoft's [Quickstart: Sentiment analysis and opinion mining](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/quickstart?pivots=programming-language-python)

## secrets.py
If you wish to use this script _(at your own risk)_, you must create a `secrets.py` file in the root directory of the project with the following variables

```python
endpoint = [Azure Cognitive Service API endpoint]
key = [Azure Cognitive Service API key]
newskey = [News API key]
```