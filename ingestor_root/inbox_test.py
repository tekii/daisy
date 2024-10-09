import pytest

#
# avoiding to put the test with the module code because loading the test run the __init__ and
# load default before the mokeypatch
#


@pytest.fixture()
def the_queue_inbox(ingestor_queue_service_account_credentials):
    import queue_inbox

    return queue_inbox


def test_configure_or_die(queue_inbox):

    delegated_credentials = queue_inbox.get_delegated_credentials_or_die(
        subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    print()

    for stream, start_history_id, message_id, message_date, attach_id, filename in queue_inbox.attachments_since(
        start_history_id=4255018, credentials=delegated_credentials
    ):
        # while True:

        # line = stream.readline()
        print(start_history_id, message_id, message_date, filename, attach_id)
        # if len(line) == 0:
        #    break
