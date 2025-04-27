import base64
import json
import os
import time

from google.auth import default, impersonated_credentials
from google.auth.transport.requests import Request
from google.oauth2 import credentials

# __all__ = ["get_subject_credentials_from_impersonated"]


# grant service Account Creator on the ingestor to the work acc
def get_subject_credentials_from_impersonated(
    # target_account_email: str,
    subject_email: str,
    subject_scopes: list[str],
    lifetime: int = 3600,
) -> credentials.Credentials:

    target_account_email = os.environ.get("INGESTOR_SERVICE_ACCOUNT_EMAIL", None)
    if target_account_email is None:
        # TODO log
        raise RuntimeError("Undefined INGESTOR_SERVICE_ACCOUNT_EMAIL")

    # subject_email = os.environ.get("INGESTOR_SUBJECT_ACCOUNT_EMAIL", None)
    # if subject_email is None:
    #     # TODO log
    #     raise RuntimeError("Undefined INGESTOR_SUBJECT_ACCOUNT_EMAIL")

    # this is test-runner or the main service account
    source_credentials, _ = default()
    # this is the intermediate service account w/ wide domain delegation granted
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=target_account_email,
        target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        lifetime=lifetime,
    )

    header = {
        "alg": "RS256",
        "typ": "JWT",
    }

    now = int(time.time())

    claim = {
        "iss": target_account_email,
        "scope": " ".join(subject_scopes),
        "aud": "https://accounts.google.com/o/oauth2/token",
        "sub": subject_email,
        "exp": now + lifetime,
        "iat": now,
    }

    header_claims = "{}.{}".format(
        base64.urlsafe_b64encode(str(header).encode()).decode().rstrip("="),
        base64.urlsafe_b64encode(str(claim).encode()).decode().rstrip("="),
    )

    signed_bytes = target_credentials.sign_bytes(header_claims.encode())

    # assertion = header_claims + "." + base64.urlsafe_b64encode(signed_bytes).decode().rstrip("=")
    assertion = f"{header_claims}.{base64.urlsafe_b64encode(signed_bytes).decode().rstrip('=')}"

    # now exchange the signed_jwt for an access_token representing the subject sub
    data = {
        "grant_type": "assertion",
        "assertion_type": "http://oauth.net/grant_type/jwt/1.0/bearer",
        "assertion": assertion,
    }

    url = "https://accounts.google.com/o/oauth2/token"
    request = Request()
    response = request(url=url, method="POST", headers=header, body=data)
    # TODO: catch TransportError and raise my own
    if response.status == 200:
        rdata = json.loads(response.data)
        access_token = rdata["access_token"]
        # expires_in = rdata["expires_in"]
        # token_type = rdata["token_type"]
        return credentials.Credentials(access_token)
    else:
        # TODO: populate the exception w/ the data of the response
        raise Exception
