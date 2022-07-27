import os
import base64
import json
import functions_framework
from flask import abort

from google.auth import default as default_credentials, iam
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account

from gmail import dummy
from helper import dummy as d2

DAISY_SUBJECT_ACCOUNTS = "DAISY_SUBJECT_ACCOUNTS"


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def the_function(cloud_event):

    # is the event type I expect?
    if cloud_event["type"] != "google.cloud.pubsub.topic.v1.messagePublished":
        abort(500, description=(f"NOT the cloud_event type expected: {str(cloud_event['type'])}"))

    # recover valid subjects to be expected
    subjects = os.getenv(DAISY_SUBJECT_ACCOUNTS)
    if subjects is None or len(subjects) == 0:
        abort(500, description=("DAISY_SUBJECT_ACCOUNTS is not set or its empty."))
    subjects = subjects.lower().split(";")

    # decode the PubSub message in the payload
    try:
        data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8"))
        subject = data["emailAddress"]
        historyId = data["historyId"]
    except (KeyError, json.JSONDecodeError) as e:
        abort(500, description=(f"Exception decoding PubSub message: {repr(e)}"))

    # validate subject
    if subject not in subjects:
        abort(500, description=("'subject' is not in DAISY_SUBJECT_ACCOUNTS."))

    #
    try:
        credentials, _ = default_credentials()
        request = requests.Request()
        credentials.refresh(request)

        signer = iam.Signer(request, credentials, credentials.service_account_email)

        updated_credentials = service_account.Credentials(
            signer,
            credentials.service_account_email,
            "https://accounts.google.com/o/oauth2/token",
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            subject=subject,
        )
    except GoogleAuthError as e:
        abort(500, description=(f"Some credentials related problem: {repr(e)}"))

    dummy()
    d2()
