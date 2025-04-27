import pytest

# from typing import Any

# import google.auth
# from google.oauth2 import service_account

# TODO https://github.com/GoogleCloudPlatform/functions-framework-python/blob/main/conftest.py


# def _default(
#    scopes: Any | None = [
#        "https://www.googleapis.com/auth/gmail.readonly",
#        "https://www.googleapis.com/auth/cloud-platform",
#    ]
# ):
#    """Replaces the current default credentials w/ de test-runner ones."""
#    credentials = service_account.Credentials.from_service_account_file(
#        "../.secrets/test-runner-credentials.json",
#        scopes=scopes,
#    )
#    return credentials, "daisy-dev01"
#
#
# @pytest.fixture(autouse=False)
# def test_runner_service_account_credentials(monkeypatch):
#    # replace curent default w/ the service account JWT
#    monkeypatch.setattr(google.auth, "default", _default)


@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    monkeypatch.setenv(
        "DATASET",
        "orange",
    )
    monkeypatch.setenv(
        "SUBJECTS",
        "PR@legacy.tekii.com.ar;QUEUE@margot.tekii.com.ar;queue@margot.tekii.com.ar",
    )
    monkeypatch.setenv(
        "INGESTOR_SERVICE_ACCOUNT_EMAIL",
        "ingestor@daisy-dev01.iam.gserviceaccount.com",
    )
    monkeypatch.setenv(
        "INGESTOR_SUBJECT_ACCOUNT_EMAIL",
        "queue@margot.tekii.com.ar",
    )

    try:

        yield

    finally:
        monkeypatch.undo()
