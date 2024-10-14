import os
import base64
import json
import logging
import functions_framework
from flask import abort

import inbox

DAISY_SUBJECT_ACCOUNTS = "DAISY_SUBJECT_ACCOUNTS"

_logger = logging.getLogger("INGESTOR")


# Triggered from a message on a Cloud Pub/Sub topic ingestor-queue.
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

        # whit this call users.history.list

    except (KeyError, json.JSONDecodeError) as e:
        abort(500, description=(f"Exception decoding PubSub message: {repr(e)}"))

    _logger.info(f"The subject is {subject}")

    # validate subject
    if subject not in subjects:
        abort(500, description=("'subject' is not in DAISY_SUBJECT_ACCOUNTS."))

    # gets the credentials with inbox access
    delegated_credentials = inbox.get_delegated_credentials_or_die(
        subject=subject, scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    # iterate over
    for stream, history_id, message_id, message_from, message_date, message_subject, attachment_id, filename in inbox.attachments_since(
        start_history_id=int(historyId), credentials=delegated_credentials
    ):
        _logger.info(f"date:{message_date} filename:{filename}")
        pass
