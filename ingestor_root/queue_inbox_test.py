import pytest

#
# avoiding to put the test with the module code because loading the test run the __init__ and
# load default before the mokeypatch
#


@pytest.fixture()
def the_ingestor_queue_under_test(ingestor_queue_service_account_credentials):
    import event_queue

    return event_queue


def test_configure_or_die(the_ingestor_queue_under_test):

    ingestor_queue = the_ingestor_queue_under_test

    delegated_credentials = ingestor_queue.get_delegated_credentials_or_die(
        subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    print()

    for stream, start_history_id, message_id, message_date, attach_id, filename in ingestor_queue.attachments_since(
        start_history_id=4255018, credentials=delegated_credentials
    ):
        # while True:

        # line = stream.readline()
        print(start_history_id, message_id, message_date, filename, attach_id)
        # if len(line) == 0:
        #    break
