from event import append_events_rows


def test_ingest(test_runner_service_account_credentials: None):
    import inbox

    table_name = "orange.append_events_rows_tests_2"
    table_id = f"{inbox.config.PROJECT}.{table_name}"

    delegated_credentials = inbox.get_delegated_credentials_or_die(
        subject="queue@margot.tekii.com.ar"
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
