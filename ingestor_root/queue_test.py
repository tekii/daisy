import pytest


from ingest import append_events_rows


@pytest.fixture()
def the_inbox(test_runner_credentials):
    # first monkeypatch the credentials, then import the module
    import inbox

    return inbox


def test_queue(the_inbox):

    inbox = the_inbox
    project_id = "daisy-dev01"
    table_name = "orange.append_events_rows_tests_2"
    table_id = f"{project_id}.{table_name}"

    delegated_credentials = inbox.get_delegated_credentials_or_die(
        subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    for stream, history_id, message_id, message_from, message_date, message_subject, attachment_id, filename in inbox.attachments_since(
        4255018, credentials=delegated_credentials
    ):

        append_events_rows(
            stream,
            destination_table=table_id,
            project_id=project_id,
            history_id=history_id,
            message_id=message_id,
            message_from=message_from,
            message_date=message_date,
            message_subject=message_subject,
            attachment_id=attachment_id,
            filename=filename,
        )
