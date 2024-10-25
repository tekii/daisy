import pytest

#
# avoiding to put the test with the module code because loading the test run the __init__ and
# load default before the mokeypatch
#


@pytest.fixture()
def the_patched_inbox(test_runner_service_account_credentials):
    # first monkeypatch the credentials, then import the module
    import inbox

    return inbox


def test_configure_or_die(the_patched_inbox):
    import inbox

    delegated_credentials = inbox.get_delegated_credentials(
        subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
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
    ) in inbox.attachments_since(start_history_id=4255018, credentials=delegated_credentials):
        # while True:

        # line = stream.readline()
        print(history_id, message_id, message_from, message_date, message_subject, attachment_id)
        # if len(line) == 0:
        #    break


def test_attachment_ids_since(the_patched_inbox):
    # this import is only for the type hint (i hope)
    import inbox

    delegated_credentials = inbox.get_delegated_credentials(
        subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    for (
        history_id,
        message_id,
        message_from,
        message_date,
        message_subject,
        attachment_id,
        filename,
    ) in inbox.attachment_ids_since(start_history_id=4255018, credentials=delegated_credentials):
        # while True:

        # line = stream.readline()
        print(history_id, message_id, message_from, message_date, message_subject, attachment_id, filename)
        print()
        # if len(line) == 0:
        #    break
