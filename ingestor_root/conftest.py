import pytest

from typing import Any

import google.auth
from google.oauth2 import service_account


def _default(scopes: Any | None = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/cloud-platform"]):

    creds = service_account.Credentials.from_service_account_file(
        "../.secrets/test-runner-credentials.json",
        scopes=scopes,
    )

    return creds, "daisy-dev01"


@pytest.fixture(autouse=False)
def test_runner_credentials(monkeypatch):
    # replace curent default w/ the service account JWT
    monkeypatch.setattr(google.auth, "default", _default)
