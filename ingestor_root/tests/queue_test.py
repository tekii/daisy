import pytest

from event import append_events_rows
from mail.delegated_credentials import get_subject_credentials_from_impersonated


@pytest.skip(allow_module_level=True)
def test_ingest():
    # import inbox

    table_name = "orange.append_events_rows_tests_2"
    table_id = f"{inbox.config.PROJECT}.{table_name}"

    delegated_credentials = get_subject_credentials_from_impersonated(
        subject_email="queue@margot.tekii.com.ar",
        subject_scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    )

    for (
        stream,
        history_id,
        message_id,
        message_from,
        message_date,
        message_subject,
        attachment_id,
        filename,
    ) in inbox.attachments_since(4255018, credentials=delegated_credentials):

        append_events_rows(
            stream,
            destination_table=table_id,
            project_id=inbox.config.PROJECT,
            history_id=history_id,
            message_id=message_id,
            message_from=message_from,
            message_date=message_date,
            message_subject=message_subject,
            attachment_id=attachment_id,
            filename=filename,
        )
