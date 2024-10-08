""" """

import logging
from google.auth import default, iam
from google.auth.transport import requests

# from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from googleapiclient.discovery import build  # type: ignore[import-untyped]
from googleapiclient.errors import HttpError  # type: ignore[import-untyped]
import base64
from io import BytesIO
from email.utils import parsedate_to_datetime

# from base64io import Base64IO

__all__ = ["get_delegated_credentials_or_die", "attachments_since"]

_delegated_credentials = None


def get_delegated_credentials_or_die(subject, scopes):

    global _delegated_credentials

    # already set?
    if _delegated_credentials is None:

        # no, then gets the default credentials for the current environment.
        credentials, _ = default()

        try:
            # this case is if the credential cames from a JWT file
            _delegated_credentials = credentials.with_subject(subject).with_scopes(scopes)

        except AttributeError:

            # Looks like we are in the cloud  Refresh the boostrap credentials. This ensures that the information
            # about this account, notably the email, is populated.
            request = requests.Request()
            credentials.refresh(request)

            # Create an IAM signer using the bootstrap credentials.
            signer = iam.Signer(request, credentials, credentials.service_account_email)

            # Create OAuth 2.0 Service Account credentials using the IAM-based
            # signer and the bootstrap_credential's service account email.
            _delegated_credentials = service_account.Credentials(
                signer=signer,
                service_account_email=credentials.service_account_email,
                token_uri="https://accounts.google.com/o/oauth2/token",
                scopes=scopes,
                subject=subject,
            )
        except Exception:
            raise

    return _delegated_credentials


# class TheIngestorQueue(object):
#    def __new__(cls):
#        if not hasattr(cls, "_the_one_and_only"):
#            cls._the_one_and_only = super().__new__(cls)
#            cls._is_already_configured: bool = False  # type: ignore[annotation-unchecked]
#            # cls._service_proxy: ServiceProxy
#
#        return cls._the_one_and_only
#
#    @classmethod
#    def configure_or_die(cls, credentials=None):
#        if not cls._is_already_configured:
#
#            credentials, project_id = default()
#
#            delegated_credentials = get_ingestor_queue_delegated_credential(
#                credentials=credentials, subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
#            )
#
#            #
#            cls._gmail_client = build("gmail", "v1", credentials=delegated_credentials)
#
#            #
#            cls._is_already_configured = True
#
#        return cls._the_one_and_only
#
#    @classmethod
#    def watch(cls):
#        topic = "projects/daisy-dev01/topics/gmail-watch"
#        label = "INBOX"
#        request = {"labelIds": [label], "topicName": topic}
#        try:
#            result = cls._gmail_client.users().watch(userId="me", body=request).execute()
#        except HttpError as error:
#            # TODO(developer) - Handle errors from gmail API.
#            print(f"An error occurred: {error}")
#
#    @classmethod
#    def stop(cls):
#        pass


def attachments_since(start_history_id, credentials):
    #
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
                                        date = parsedate_to_datetime(value)
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
                                            yield (
                                                stream,
                                                str(start_history_id),
                                                message_id,
                                                date,
                                                attachment_id,
                                                filename,
                                            )

                                        except GeneratorExit:
                                            # TODO handle the exit vs nextPageToken?
                                            pass  # break
                                        finally:
                                            pass
                                            # log something

                                    else:
                                        continue

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
