#
"""
Validate the authenticated s2s request from chat.
"""

# from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token
from werkzeug.exceptions import Unauthorized

# Bearer Tokens received by apps will always specify this issuer.
_CHAT_ISSUER = "chat@system.gserviceaccount.com"
# Url to obtain the public certificate for the issuer.
_PUBLIC_CERT_URL_PREFIX = "https://www.googleapis.com/service_accounts/v1/metadata/x509/"


def validate_chat_authorization(
    request,
    audience=None,
):
    """ """

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise Unauthorized("Missing Authorization Header")

    auth_type, encoded_token = auth_header.split(" ", 1)
    if auth_type.lower() != "bearer":
        raise Unauthorized(f"Unhandled header format ({auth_type})")

    try:
        decoded_token = id_token.verify_token(
            id_token=encoded_token,
            audience=audience,
            certs_url=_PUBLIC_CERT_URL_PREFIX + _CHAT_ISSUER,
            request=requests.Request(),
        )
    except ValueError as e:
        # TODO: sure there is a better way...
        raise Unauthorized(str(e))

    if decoded_token["iss"] not in [_CHAT_ISSUER]:  # add test user here
        raise Unauthorized("Wrong issuer. 'iss' should be one of the following: {}".format(_CHAT_ISSUER))

    return decoded_token
