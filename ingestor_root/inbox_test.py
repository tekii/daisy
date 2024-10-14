import pytest

#
# avoiding to put the test with the module code because loading the test run the __init__ and
# load default before the mokeypatch
#


@pytest.fixture()
def the_inbox(test_runner_credentials):
    # first monkeypatch the credentials, then import the module
    import inbox

    return inbox


def test_configure_or_die(the_inbox):

    delegated_credentials = the_inbox.get_delegated_credentials_or_die(
        subject="queue@margot.tekii.com.ar", scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    for stream, history_id, message_id, message_from, message_date, message_subject, attachment_id, filename in the_inbox.attachments_since(
        start_history_id=4255018, credentials=delegated_credentials
    ):
        # while True:

        # line = stream.readline()
        print(history_id, message_id, message_from, message_date, message_subject, attachment_id)
        # if len(line) == 0:
        #    break
