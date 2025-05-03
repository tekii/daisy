import pytest

import mail.queue


@pytest.fixture(autouse=True)
def subject_credentials(delegate_credentials):

    from mail.delegated_credentials import get_subject_credentials_from_impersonated

    credentials = get_subject_credentials_from_impersonated(
        delegate=delegate_credentials,
        subject_email="queue@margot.tekii.com.ar",
        subject_scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        lifetime=360,
    )

    # create the client to get the mails
    yield credentials


def test_for_each_mail_and_each_attachment(subject_credentials):

    start_history_id = 4365464

    queue = mail.queue.Queue(credentials=subject_credentials)

    for message_id, history_id in queue.each_messages_added_since(
        start_history_id=start_history_id
    ):
        assert message_id != 0
        assert history_id is not None
        break

    for attachment_data in queue.each_attachment_in_message(message_id=message_id):

        assert attachment_data.message_id != 0
        break

    stream = queue.get_attachment(
        attachment_id=attachment_data.attachment_id, message_id=attachment_data.message_id
    )

    data = stream.read()
    pass


def test_expired_history_id(subject_credentials):

    start_history_id = 4203500

    queue = mail.queue.Queue(credentials=subject_credentials)

    with pytest.raises(mail.queue.HistoryIdExpiredError) as e:
        for message_id, history_id in queue.each_messages_added_since(
            start_history_id=start_history_id
        ):
            assert message_id != 0
            assert history_id is not None
            break
    assert e.type == mail.queue.HistoryIdExpiredError
    # assert e.status == 404
