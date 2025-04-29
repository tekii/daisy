import base64
import json
import logging
from os import getenv

import functions_framework
from flask import abort, jsonify
from google.auth import default, impersonated_credentials
from googleapiclient.discovery import build  # type: ignore[import-untyped]

# import attachment
import history

# from helpers import configuration as config
from mail.delegated_credentials import get_subject_credentials_from_impersonated
from mail.history import (
    each_attachment_in_message,
    each_messages_added_since,
    get_attachment,
)

if __name__ != "__main__" and __name__ != "__test__":
    import google.cloud.logging

    labels = {"margot_service": "ingestor"}
    logging_client = google.cloud.logging.Client()
    logging_client.setup_logging(labels=labels)


@functions_framework.errorhandler(503)
def handle_(e):
    msg = f"Some ConnectionError: {e.args}."
    logging.error(msg=msg)
    return jsonify({"errorMessage": msg}), 503


# @functions_framework.errorhandler()
# def handle_exception(e):
#
#    msg = " "
#    error = {
#        "errorType": "MARGARITA",
#        "errorCode": e.errorCode,
#        "errorArgs": e.errorArgs,
#        # "errorTimeStamp": datetime.now(timezone.utc).isoformat(),
#    }
#    labels = {"margarita_code": f"{e.errorCode}"}
#    logging.log(
#        level=e.level,
#        msg=msg,
#        extra={
#            "labels": labels,
#            "json_fields": error,
#        },
#    )
#    return jsonify([error]), e.code


# Triggered from a message on a Cloud Pub/Sub topic ingestor-queue.
@functions_framework.cloud_event
def the_function(cloud_event):
    global _SUBJECTS
    global _INGESTOR_SERVICE_ACCOUNT_EMAIL

    # is the event type I expect?
    if cloud_event["type"] != "google.cloud.pubsub.topic.v1.messagePublished":
        abort(
            500,
            f"NOT the cloud_event type expected: {str(cloud_event['type'])}",
        )

    # decode the PubSub message in the payload
    try:
        data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8"))
        subject = data["emailAddress"]
        new_history_id = data["historyId"]

    except (
        KeyError,
        json.JSONDecodeError,
    ) as e:
        abort(
            500,
            description=(f"Exception decoding PubSub message: {repr(e)}"),
        )

    # this is test-runner or the service account
    source_credentials, _ = default()
    # this is the intermediate service account w/ wide domain delegation granted
    # and access to the history_id table
    delegate_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=_INGESTOR_SERVICE_ACCOUNT_EMAIL,
        target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        lifetime=3600,
    )

    # validate subject
    subjects = _SUBJECTS.lower().split(";")
    if subject not in subjects:
        abort(500, description=(f"'{subject}' is not in SUBJECTS."))

    logging.info(f"The inbox subject is {subject}")

    # gets the credentials with the queue inbox access
    subject_credentials = get_subject_credentials_from_impersonated(
        delegate=delegate_credentials,
        subject_email=subject,
        subject_scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    )

    # create the client to get the mails
    client = build("gmail", "v1", credentials=subject_credentials)

    # recover the previus historyId
    last_history_id = history.get_id()
    if last_history_id is not None:
        # iterate over
        for message_id, _ in each_messages_added_since(
            start_history_id=last_history_id,
            client=client,
        ):
            #
            for attachment_data in each_attachment_in_message(
                message_id=message_id,
                client=client,
            ):
                logging.log(
                    level=logging.INFO,
                    msg=f"msg_id:{attachment_data.message_id} date:{attachment_data.message_date}"
                    " filename:{attachment_data.filename}",
                    extra={},
                )
                logging.info(
                    f"msg_id:{attachment_data.message_id} date:{attachment_data.message_date}"
                    f" filename:{attachment_data.filename}"
                )
                #
                stream = get_attachment(
                    attachment_id=attachment_data.attachment_id,
                    message_id=attachment_data.message_id,
                    client=client,
                )

                # attachment.insert(attachment_data)

    # TODO when is ok to find None here?
    if new_history_id is not None:
        # save the new history_id
        history.save_id(new_history_id)


_INGESTOR_SERVICE_ACCOUNT_EMAIL: str = getenv("INGESTOR_SERVICE_ACCOUNT_EMAIL", None)
if _INGESTOR_SERVICE_ACCOUNT_EMAIL is None:
    # TODO log
    logging.fatal("INGESTOR_SERVICE_ACCOUNT_EMAIL is not defined.")
    exit(1)

_SUBJECTS = getenv("SUBJECTS")
if _SUBJECTS is None:
    logging.fatal("SUBJECTS is not defined.")
    exit(1)
