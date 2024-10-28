from os import getenv
from sys import exit
import base64
import json
import functions_framework
from flask import abort

from helpers import configuration as config
import inbox
import history
import attachment


# Triggered from a message on a Cloud Pub/Sub topic ingestor-queue.
@functions_framework.cloud_event
def the_function(cloud_event):

    # is the event type I expect?
    if cloud_event["type"] != "google.cloud.pubsub.topic.v1.messagePublished":
        abort(500, description=(f"NOT the cloud_event type expected: {str(cloud_event['type'])}"))

    # decode the PubSub message in the payload
    try:
        data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8"))
        subject = data["emailAddress"]
        new_history_id = data["historyId"]

    except (
        KeyError,
        json.JSONDecodeError,
    ) as e:
        abort(500, description=(f"Exception decoding PubSub message: {repr(e)}"))

    # validate subject
    subjects = config.SUBJECTS.lower().split(";")
    if subject not in subjects:
        abort(500, description=(f"'{subject}' is not in SUBJECTS."))
    #
    config.logger.info(f"The inbox subject is {subject}")
    # gets the credentials with the queue inbox access, TODO cache this credential for future
    inbox_credentials = inbox.get_delegated_credentials(subject=subject)

    # recover the previus historyId
    last_history_id = history.get_id()
    if last_history_id is not None:
        # iterate over
        for attachment_data in inbox.each_attachment_data_since(
            start_history_id=last_history_id,
            credentials=inbox_credentials,
        ):
            config.logger.info(
                f"msg_id:{attachment_data.message_id} date:{attachment_data.message_date} filename:{attachment_data.filename}"
            )
            attachment.insert(attachment_data)

    if new_history_id is not None:
        # save the new history_id
        history.save_id(new_history_id)
