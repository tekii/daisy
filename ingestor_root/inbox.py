""" """

from typing import NamedTuple
from google.auth import default as default_credentials, iam
from google.auth.transport import requests

# from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from googleapiclient.discovery import build  # type: ignore[import-untyped]
from googleapiclient.errors import HttpError  # type: ignore[import-untyped]
import base64
from io import BytesIO
from datetime import datetime
from email.utils import parsedate_to_datetime
from helpers import configuration as config

__all__ = ["get_delegated_credentials", "attachments_since", "each_attachment_data_since"]


_delegated_credentials = None


class AttachmentData(NamedTuple):
    history_id: int
    message_id: str
    message_from: str | None
    message_date: datetime | None
    message_subject: str | None
    attachment_id: str
    filename: str


def get_delegated_credentials(
    subject,
    scopes=["https://www.googleapis.com/auth/gmail.readonly"],
):

    global _delegated_credentials

    # already set?
    if _delegated_credentials is None:

        # no, then gets the default credentials for the current environment.
        credentials, _ = default_credentials()

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
        # except GoogleAuthError as e:
        #    _logger.exception(e)  #    f"Some credentials related problem: {repr(e)}"
        #    raise

        except Exception:
            # TODO
            raise

    return _delegated_credentials


def attachments_since(start_history_id, credentials):
    #
    config.logger.info(f"Attempting to retrieve history since {str(start_history_id)}.")

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
                            header_subject = None
                            header_date = None
                            header_from = None
                            for header in headers:
                                match header:
                                    case {"name": "Subject", "value": value}:
                                        header_subject = value
                                    case {"name": "Date", "value": value}:
                                        # header_date = value
                                        header_date = parsedate_to_datetime(value)
                                    case {"name": "From", "value": value}:
                                        header_from = value
                                    case {"name": "Subject", "value": value}:
                                        header_subject = value

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
                                            config.logger.info(f"Yielding attachment {filename}.")
                                            #
                                            yield (
                                                stream,
                                                # str(start_history_id),
                                                start_history_id,
                                                message_id,
                                                header_from,
                                                header_date,
                                                header_subject,
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
        # TODO handle expired history ids
        config.logger.error(f"Error retriving history {e.reason}")
        # if e.resp.status in [403, 404, 500, 503]:
        #    pass
        # else:
        # log the error
        raise e


def each_attachment_data_since(start_history_id: int, credentials):
    # this function has no state of its own, its depend entirely on someone store the start_history_id outside
    #
    config.logger.info(f"Attempting to retrieve attachment ids since {str(start_history_id)}.")

    client = build("gmail", "v1", credentials=credentials)

    try:
        # set the history pagination
        pageToken = None
        # iterate over pages of this historyId
        while True:
            #
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
            if history is not None:
                for history_record in history:
                    messages_added = history_record.get("messagesAdded")
                    # this check only make sense if the watch was incorrectly setup
                    if messages_added is not None:
                        for message_added in messages_added:
                            message_id: str = message_added["message"]["id"]
                            # recover the actual message
                            message = client.users().messages().get(userId="me", id=message_id).execute()

                            # cherry pick headers
                            headers = message["payload"]["headers"]
                            header_subject = None
                            header_date = None
                            header_from = None
                            for header in headers:
                                match header:
                                    case {"name": "Subject", "value": value}:
                                        header_subject = value
                                    case {"name": "Date", "value": value}:
                                        # header_date = value
                                        header_date = parsedate_to_datetime(value)
                                    case {"name": "From", "value": value}:
                                        header_from = value
                                    case {"name": "Subject", "value": value}:
                                        header_subject = value

                            # check payload mimeType
                            for part in message["payload"]["parts"]:
                                #
                                try:

                                    filename = part["filename"]
                                    if filename is not None and len(filename) != 0:
                                        # body = part.get("body")
                                        # attachment_id = body.get("attachmentId")
                                        attachment_id = part["body"]["attachmentId"]

                                        try:
                                            #
                                            config.logger.info(f"Yielding attachment {filename}.")

                                            yield AttachmentData(
                                                start_history_id,
                                                message_id,
                                                header_from,
                                                header_date,
                                                header_subject,
                                                attachment_id,
                                                filename,
                                            )

                                        except GeneratorExit:
                                            # TODO handle the exit vs nextPageToken?
                                            break

                                        finally:
                                            pass
                                            # log something

                                    else:
                                        continue

                                except KeyError:
                                    # log the error
                                    continue

            # next page
            pageToken = results.get("nextPageToken")
            # TODO log this --> new_history_id = results.get("historyId")
            if not pageToken:
                break

    except HttpError as e:
        # TODO handle expired history ids
        config.logger.error(f"Error retriving history {e.reason}")
        # if e.resp.status in [403, 404, 500, 503]:
        #    pass
        # else:
        # log the error
        raise e
