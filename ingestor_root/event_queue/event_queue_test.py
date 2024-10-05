import pytest

from . import get_queue_attachments_since

import google.auth
from google.oauth2 import service_account


@pytest.fixture(autouse=False)
def mock_credentials(monkeypatch):

    monkeypatch.setattr(
        google.auth,
        "default",
        lambda: (
            service_account.Credentials.from_service_account_file(
                "../../.secrets/mock_credentials.json",
                # scopes=["https://www.googleapis.com/auth/cloud-platform"],
                scopes=["https://www.googleapis.com/auth/gmail.readonly"],
                subject="queue@margot.tekii.com.ar",
            ),
            None,
        ),
    )


def test_get():

    for stream, start_history_id, message_id, message_date, attach_id, filename in get_queue_attachments_since(4255018):
        while True:

            # line = stream.readline()
            # print(line, id, filename, date)
            # if len(line) == 0:
            #    break

            pass
