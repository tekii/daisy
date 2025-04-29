import base64
import json
import time

from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.oauth2 import credentials

# __all__ = ["get_subject_credentials_from_impersonated"]


# grant service Account Creator on the ingestor to the work acc
def get_subject_credentials_from_impersonated(
    delegate: impersonated_credentials.Credentials,
    # target_account_email: str,
    subject_email: str,
    subject_scopes: list[str],
    lifetime: int = 3600,
) -> credentials.Credentials:

    header = {
        "alg": "RS256",
        "typ": "JWT",
    }

    now = int(time.time())

    claim = {
        "iss": delegate.service_account_email,
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

    signed_bytes = delegate.sign_bytes(header_claims.encode())

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
