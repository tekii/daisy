import pytest

from google.oauth2 import service_account

from gmail import get_queue_attachments_since
from ingest import append_events_rows


def test_queue():

    project_id = "daisy-dev01"
    table_name = "orange.append_events_rows_tests"
    table_id = f"{project_id}.{table_name}"

    scopes = "https://www.googleapis.com/auth/gmail.readonly"
    credentials = service_account.Credentials.from_service_account_file(
        "../.secrets/mock_credentials.json", scopes=[scopes], subject="queue@margot.tekii.com.ar"
    )

    for stream, start_history_id, message_id, message_date, attach_id, filename in get_queue_attachments_since(
        4255018, credentials=credentials
    ):

        append_events_rows(
            stream,
            destination_table=table_id,
            project_id=project_id,
            start_history_id=start_history_id,
            message_id=message_id,
            message_date=message_date,
            attach_id=attach_id,
            filename=filename,
        )
