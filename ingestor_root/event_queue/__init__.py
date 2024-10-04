""" """

import logging

# from google.auth import default as default_credentials
# from google.auth.exceptions import GoogleAuthError
# from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from io import BytesIO

# from base64io import Base64IO


__all__ = ["get_queue_attachments_since"]


def get_queue_attachments_since(start_history_id, credentials=None):
    # credentials, _ = default_credentials()
    # scopes = "https://www.googleapis.com/auth/gmail.readonly"
    # credentials = service_account.Credentials.from_service_account_file(
    #    "../.secrets/mock_credentials.json", scopes=[scopes], subject="queue@margot.tekii.com.ar"
    # )
    ##

    logging.info(f"Attempting to retrieve history since {str(start_history_id)}.")

    client = build("gmail", "v1", credentials=credentials)

    try:
        # set the history pagination
        pageToken = None
        # iterate over pages of this historyId
        while True:
            # 4203500 4255018
            results = (
                client.users()
                .history()
                .list(
                    userId="me",
                    startHistoryId=start_history_id,
                    labelId="INBOX",
                    historyTypes=["messageAdded"],
                    maxResults=10,
                    pageToken=pageToken,
                )
                .execute()
            )

            # TODO check this
            #   list = history.list_next(previous_request=list, previous_response=response)

            history = results.get("history")
            if history:
                for history_record in history:
                    messages_added = history_record.get("messagesAdded")
                    if messages_added:
                        for message_added in messages_added:
                            message_id = message_added["message"]["id"]
                            message = client.users().messages().get(userId="me", id=message_id).execute()
                            # cherry pick headers
                            headers = message["payload"]["headers"]
                            subject = None
                            date = None
                            from_ = None
                            for header in headers:
                                match header:
                                    case {"name": "Subject", "value": value}:
                                        subject = value
                                    case {"name": "Date", "value": value}:
                                        date = value
                                    case {"name": "From", "value": value}:
                                        from_ = value

                            # check payload mimeType
                            for part in message["payload"]["parts"]:
                                filename = part["filename"]
                                if filename != None and filename != "":
                                    body = part.get("body")

                                    # this case never happens
                                    data = body.get("data")
                                    # if data:
                                    #    toto = data
                                    attachment_id = body.get("attachmentId")
                                    if attachment_id:
                                        attachment = (
                                            client.users()
                                            .messages()
                                            .attachments()
                                            .get(userId="me", id=attachment_id, messageId=message_id)
                                            .execute()
                                        )
                                        data = attachment["data"]

                                        lines = base64.b64decode(data)
                                        stream = BytesIO(lines)

                                        # with StringIO(data) as encoded_stream:
                                        # with BytesIO(data) as encoded_stream:
                                        #    with Base64IO(encoded_stream) as stream:
                                        try:
                                            #
                                            logging.info(f"Yielding attachment {filename}.")
                                            #
                                            yield (stream, str(start_history_id), message_id, date, attachment_id, filename)

                                        except GeneratorExit:
                                            pass  # break

                                        finally:
                                            pass
                                            # log something

            pageToken = results.get("nextPageToken")
            if not pageToken:
                break

    except HttpError as e:
        logging.error(f"Error retriving history {e.reason}")
        # if e.resp.status in [403, 404, 500, 503]:
        #    pass
        # else:

        # log the error
        raise e
