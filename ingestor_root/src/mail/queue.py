import base64
import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from io import BytesIO
from typing import NamedTuple

# from google.auth.exceptions import GoogleAuthError
from googleapiclient.discovery import build  # type: ignore[import-untyped]
from googleapiclient.errors import HttpError  # type: ignore[import-untyped]

# from helpers import configuration as

__all__ = [
    "Queue",
    "AttachmentData",
    "HistoryIdExpiredError",
]


class HistoryIdExpiredError(Exception):
    history_id: int


class AttachmentData(NamedTuple):
    history_id: int
    message_id: str
    message_from: str | None
    message_date: datetime | None
    message_subject: str | None
    attachment_id: str
    filename: str


class Queue:
    """mail queue"""

    def __init__(self, credentials):
        self._client = build("gmail", "v1", credentials=credentials)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._client.__exit__(exc_type, exc_value, traceback)

    def each_messages_added_since(self, start_history_id: int):
        # this function has no state of its own, its depend entirely on someone store the
        # start_history_id outside
        logging.info(f"Attempting to retrieve attachment ids since {str(start_history_id)}.")

        # set the history pagination
        pageToken = None
        # iterate over pages of this historyId
        while True:
            #
            try:
                results = (
                    self._client.users()
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

            except HttpError as e:
                # 404 here means the history_id is expired see
                # https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.history/list#query-parameters
                if e.resp.status == 404:
                    h = HistoryIdExpiredError()
                    h.history_id = start_history_id
                    raise h from e
                else:
                    raise e

            # TODO check this
            #   list = history.list_next(previous_request=list, previous_response=response)
            history = results.get("history")
            history_id = results.get("historyId")
            if history is not None:
                for history_record in history:
                    messages_added = history_record.get("messagesAdded")
                    # this check only make sense if the watch was incorrectly setup
                    if messages_added is not None:
                        for message_added in messages_added:
                            message_id: str = message_added["message"]["id"]

                            yield message_id, history_id
            # next page
            pageToken = results.get("nextPageToken")
            # TODO log this --> new_history_id = results.get("historyId")
            if not pageToken:
                break

    def each_attachment_in_message(self, message_id: str):

        # recover the actual message
        message = self._client.users().messages().get(userId="me", id=message_id).execute()
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
            try:
                filename = part["filename"]
                if filename is not None and len(filename) != 0:
                    # body = part.get("body")
                    # attachment_id = body.get("attachmentId")
                    attachment_id = part["body"]["attachmentId"]

                    try:
                        #
                        logging.info(f"Yielding attachment {filename}.")

                        yield AttachmentData(
                            1,  # start_history_id,
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

    def get_attachment(self, attachment_id: str, message_id: str) -> BytesIO:

        attachment = (
            self._client.users()
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
        return stream
