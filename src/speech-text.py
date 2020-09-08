#!/usr/bin/env python
# coding: utf-8
import os
from typing import List
import logging
import sys
import requests
import time
import swagger_client as cris_client
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")

SPEECH_KEY = os.getenv('SPEECH_API_SUBSCRIPTION_KEY')
SERVICE_REGION = 'westus2'
NAME = "Test transcription"
DESCRIPTION = "Test transcription description"
LOCALE = 'en-US'
RECORDINGS_BLOB_URI = 'https://devguideblob.blob.core.windows.net/tailwindtradersblob?sv=2019-02-02&st=2020-08-31T18%3A31%3A41Z&se=2020-10-31T18%3A31%3A00Z&sr=c&sp=rawl&sig=AL8bA7jbHr8vsRtp2A4Z5fNWxYQWTuWnvqNICUJHS8w%3D'


def transcribe():
    logging.info("Starting transcription client...")

    configuration = cris_client.Configuration()
    configuration.api_key['Ocp-Apim-Subscription-Key'] = SPEECH_KEY
    configuration.host = "https://{}.cris.ai".format(SERVICE_REGION)

    # create the client object and authenticate
    client = cris_client.ApiClient(configuration)

    # create an instance of the transcription api class
    transcription_api = cris_client.CustomSpeechTranscriptionsApi(api_client=client)

    transcription_definition = cris_client.TranscriptionDefinition(
        name=NAME, description=DESCRIPTION, locale=LOCALE, recordings_url=RECORDINGS_BLOB_URI
    )

    data, status, headers = transcription_api.create_transcription_with_http_info(transcription_definition)

    # extract transcription location from the headers
    transcription_location: str = headers["location"]

    # get the transcription Id from the location URI
    created_transcription: str = transcription_location.split('/')[-1]

    logging.info("Created new transcription with id {}".format(created_transcription))

    logging.info("Checking status.")

    completed = False

    while not completed:
        running, not_started = 0, 0

        # get all transcriptions for the user
        transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()

        # for each transcription in the list we check the status
        for transcription in transcriptions:
            if transcription.status in ("Failed", "Succeeded"):
                # we check to see if it was the transcription we created from this client
                if created_transcription != transcription.id:
                    continue

                completed = True

                if transcription.status == "Succeeded": 
                    results_uri = transcription.results_urls["channel_0"]
                    results = requests.get(results_uri)
                    logging.info("Transcription succeeded. Results: ")
                    logging.info(results.content.decode("utf-8"))
                else:
                    logging.info("Transcription failed :{}.".format(transcription.status_message))
                    break
            elif transcription.status == "Running":
                running += 1
            elif transcription.status == "NotStarted":
                not_started += 1

        logging.info("Transcriptions status: "
                "completed (this transcription): {}, {} running, {} not started yet".format(
                    completed, running, not_started))

        # wait for 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    load_dotenv()
    transcribe()
