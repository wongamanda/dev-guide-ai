import os
from pprint import pprint
import numpy as np
import pandas as pd
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv


def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint= endpoint, credential=ta_credential)
    return text_analytics_client


def sentiment_analysis(client, data, headers):
    sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
    sentiments = []

    for index, row in data.iterrows():
        documents = {'documents': [{'language':'en', 'id':index, 'text':row["Text"]}]}
        response = requests.post(sentiment_url, headers=headers, json=documents)
        response = response.json()
        sentiment_response = response['documents'][0]['sentiment']
        sentiments.append(sentiment_response)
    sentiments = pd.DataFrame(sentiments, columns=['Sentiment'])
    return sentiments


def extract_key_phrases(client, data, headers):
    keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"
    key_phrases = []

    for index, row in data.iterrows():
        documents = {'documents': [{'language':'en', 'id':index, 'text':row["Text"]}]}
        response = requests.post(keyphrase_url, headers=headers, json=documents)
        response = response.json()
        key_phrase_response = response['documents'][0]['keyPhrases']
        key_phrases.append(str(key_phrase_response))
    key_phrases = pd.DataFrame(key_phrases, columns=['Key Phrases'])
    return key_phrases

          
# def get_requests(documents, documents_tuples):
#     client = authenticate_client()
#     sentiments = sentiment_analysis(client, documents)
#     key_phrases = extract_key_phrases(client, documents)
#     identify_entities(client, documents)

#     for i in range(len(documents.documents) % 10):
#         documents[i:i+10]
#         sentiment_analysis(client, documents)
#         extract_key_phrases(client, documents)
    

if __name__ == "__main__":
    try:
        load_dotenv()

        subscription_key = os.getenv('SUBSCRIPTION_KEY')
        endpoint = os.getenv('ENDPOINT')
        
        azure_storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        source = "https://devguideblob.blob.core.windows.net/tailwindtradersblob/temp_table_test.csv?sv=2019-02-02&st=2020-08-28T19%3A39%3A37Z&se=2020-11-29T20%3A39%3A00Z&sr=b&sp=rw&sig=9Kl0SzHg%2Br1ggn5enff%2BccXT8VDgT0GNKTsi7V8vsNw%3D"
        blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}

        data = pd.read_csv(source, encoding="UTF-8", low_memory=False)
        data = data.dropna()
        data = data.loc[:, ['SupportTicketID','CustomerID','Theme','Text']].head(5) 

        client = authenticate_client()
        
        data['Sentiment'] = sentiment_analysis(client, data, headers)
        data['Key Phrases']= extract_key_phrases(client, data, headers)

        data.to_csv('new_data.csv', index=False)
    
    except Exception as ex:
        print(ex)