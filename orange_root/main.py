import logging
from flask import jsonify, abort
from requests import Timeout
import functions_framework

from marshalled_api import *


# logging.getLogger().setLevel(logging.INFO)


def recover_agent_credentials():
    import json
    from google.auth import default as default_credentials  # mypy: --disable-error-code=import-untyped
    from google.cloud import secretmanager

    # recover the project id of the active project
    _, project_id = default_credentials()
    #
    client = secretmanager.SecretManagerServiceClient()
    # project_id = "daisy-dev01"
    name = f"projects/{project_id}/secrets/AGENT_CREDENTIALS/versions/latest"
    response = client.access_secret_version(name=name)
    # if the proper secret its not defined is a FATAL/CRITICAL and the function should terminate immidiatly
    # return the decoded payload.
    secret_data = response.payload.data.decode("UTF-8")
    secret = json.loads(secret_data)
    # TODO: some structural check here to avoid an error or the need of checking in the call itself
    if secret["version"] == "2":
        return secret["credentials"]
    else:
        None


# the problem initializing this here is that we dont want to run this before the monkeypatch
_AGENT_CREDENTIALS = None

# TODO, implement some catch all handler that return the expected JSON


@functions_framework.errorhandler(Timeout)
def handle_timeout_error(e):
    msg = f"Some timeout error: {e.args}."
    logging.error(msg=msg)
    return jsonify({"errorMessage": msg}), 408


@functions_framework.errorhandler(MarshalError)
def handle_marshal_error(e):
    msg = f"Some Error [un]marshalling the args or the response: {e.args}."
    logging.error(msg=msg)
    return jsonify({"errorMessage": msg}), e.code


@functions_framework.errorhandler(400)
def handle_400(e):
    # 400 Bad Request
    # BigQuery will not retry this request
    logging.error(msg=e.description)
    return jsonify({"errorMessage": e.description}), 400


@functions_framework.errorhandler(401)
def handle_401(e):
    # 401 Unauthorized
    # BigQuery will not retry this request
    logging.error(msg=e.description)
    return jsonify({"errorMessage": e.description}), 401


# BigQuery WILL retry this ones
# 408 Request Timeout
# 429 Too Many Requests (RFC 6585)
# 500 Internal Server Error
# 503 Service Unavailable
# 504 Gateway Timeout


@functions_framework.http
def the_function(request):
    # pylint: disable=W0603
    global _AGENT_CREDENTIALS
    if _AGENT_CREDENTIALS is None:
        _AGENT_CREDENTIALS = recover_agent_credentials()
    #
    request_json = request.get_json()
    # setup from udc
    udc_mock_data = False
    udc_modes = None  # full | stripped
    udc_log_diagnostics = None
    udc_operation = None  # todo, change to default
    try:
        udc = request_json["userDefinedContext"]
        # which soap op to invoke
        udc_soap_operation = udc["soap_operation"]
        # udc_mode = udc["mode"] if "mode" in udc:
        udc_mock_data = "mock_data" in udc
        udc_log_diagnostics = "enable_diagnostic" in udc
    except KeyError as e:
        abort(400, f"Missing key {e} accesing userDefinedContext.")

    # which operation
    operation: Marshal | None = get_marshal(udc_soap_operation)
    if operation is None:
        abort(400, f"Unkown soap operation{udc_soap_operation}.")

    # recover the calls arguments array
    calls = request_json.get("calls")
    if calls is None:
        abort(400, "Missing UDC calls key in the request.")

    # iterate over the calls
    replies = []
    for call_args in calls:
        # first is the agent to use
        agent = call_args[0]
        # credentials 4 this call
        agent_credentials = _AGENT_CREDENTIALS.get(agent)
        # unfortunatly we los all replies if this fails. this is an non critical because only this agent is undef/unauth
        if agent_credentials is None:
            abort(401, f"Unauthorized or undefined credentials for agent: {agent}")

        replies.append(operation(*call_args, agent_credentials=agent_credentials, mock_data=udc_mock_data))

    # https://cloud.google.com/bigquery/docs/remote-functions#http_response_code
    # https://cloud.google.com/bigquery/docs/remote-functions#output_format
    return jsonify({"replies": replies})


# Your endpoint should return the HTTP response code 200 for a successful response.
# When BigQuery receives any other value, BigQuery considers the response as a failure,
# and retries when the HTTP response code is 408, 429, 500, 503 or 504 until some internal limit.
#
# if __name__ == "__main__":
#    pass
# if __name__ == "__test__":
#    pass
# else:
# import google.cloud.logging
#
# _client = google.cloud.logging.Client()
# _client.setup_logging(log_level=logging.INFO)
