import pytest

import mail.history


@pytest.fixture(autouse=True)
def authorized_client():
    from googleapiclient.discovery import build  # type: ignore[import-untyped]

    from mail.delegated_credentials import get_subject_credentials_from_impersonated

    credentials = get_subject_credentials_from_impersonated(
        subject_email="queue@margot.tekii.com.ar",
        subject_scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        lifetime=360,
    )

    # create the client to get the mails
    yield build("gmail", "v1", credentials=credentials)


def test_for_each_mail_and_each_attachment(authorized_client):

    start_history_id = 4365464

    for message_id, history_id in mail.history.each_messages_added_since(
        start_history_id=start_history_id,
        client=authorized_client,
    ):
        assert message_id != 0
        assert history_id is not None
        break

    for attachment_data in mail.history.each_attachment_in_message(
        message_id=message_id,
        client=authorized_client,
    ):

        assert attachment_data.message_id != 0
        break

    stream = mail.history.get_attachment(
        attachment_id=attachment_data.attachment_id,
        message_id=attachment_data.message_id,
        client=authorized_client,
    )

    data = stream.read()
    pass


def test_expired_history_id(authorized_client):

    start_history_id = 4203500

    with pytest.raises(mail.history.HistoryIdExpiredError) as e:
        for message_id, history_id in mail.history.each_messages_added_since(
            start_history_id=start_history_id,
            client=authorized_client,
        ):
            assert message_id != 0
            assert history_id is not None
            break
    assert e.type == mail.history.HistoryIdExpiredError
    # assert e.status == 404
