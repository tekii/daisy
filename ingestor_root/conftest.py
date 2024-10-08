import pytest
import google.auth
from google.oauth2 import service_account


@pytest.fixture(autouse=False)
def ingestor_queue_service_account_credentials(monkeypatch):
    #
    monkeypatch.setattr(
        google.auth,
        "default",
        lambda: (
            service_account.Credentials.from_service_account_file(
                "../.secrets/ingestor_queue_credentials.json",
                scopes=["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/cloud-platform"],
            ),
            "daisy-dev01",
        ),
    )
