import pytest
import google.auth
from google.oauth2 import service_account


@pytest.fixture(autouse=False)
def mock_credentials(monkeypatch):

    monkeypatch.setattr(
        google.auth,
        "default",
        lambda: (
            service_account.Credentials.from_service_account_file(
                "../.secrets/mock_credentials.json",
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            ),
            None,
        ),
    )
