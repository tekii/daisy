import logging
import functions_framework
from flask import jsonify, abort

# from trazamed import getRelay
import mock


def recover_agent_gredentials():
    # pylint: disable=C0415
    import json

    # from google.cloud import secretmanager
    #
    ## Create the Secret Manager client.
    # client = secretmanager.SecretManagerServiceClient()
    ## Build the resource name of the secret version.
    # project_id = "daisy-dev01"
    # name = f"projects/{project_id}/secrets/AGENT_CREDENTIALS/versions/latest"
    # response = client.access_secret_version(name=name)
    ## Return the decoded payload.
    # secret = response.payload.data.decode("UTF-8")
    secret = json.dumps({"glnws": {"user": "pruebasws", "pass": "Clave1234"}})
    return json.loads(secret)


AGENT_CREDENTIALS = None


@functions_framework.errorhandler(ZeroDivisionError)
def handle_zero_division(e):
    return jsonify({"errorMessage": "I'm a teapot"}), 418


@functions_framework.errorhandler(400)
def handle_400(e):
    # logging.critical(msg=msg)
    return jsonify({"errorMessage": e.description}), 400


@functions_framework.errorhandler(401)
def handle_401(e):
    # logging.critical(msg=msg)
    return jsonify({"errorMessage": e.description}), 401


@functions_framework.http
def the_function(request):
    try:
        # pylint: disable=W0603
        global AGENT_CREDENTIALS
        if AGENT_CREDENTIALS is None:
            AGENT_CREDENTIALS = recover_agent_gredentials()

        request_json = request.get_json()

        # setup from udc
        udc_mock_data = False
        udc_modes = None
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

        # get the soap operation to call
        operation = mock.get_relay(udc_soap_operation)

        # recover the calls arguments array
        calls = request_json.get("calls")
        if calls is None:
            abort(400, "Missing [calls].")

        # iterate over the calls
        replies = []
        for call_args in calls:
            # first is the agent to use
            agent = call_args[0]
            # credentials 4 this call
            credentials = AGENT_CREDENTIALS.get(agent)
            # unfortunatly we los all replies if this fails.
            if credentials is None:
                abort(401, f"Unauthorized agent: {agent}")

            r = operation(credentials, call_args)
            # encode response
            # https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type
            replies.append(r)
            # return_value.append(sum([int(x) if isinstance(x, str) else x for x in call if x is not None]))

        # replies = [str(x) if x > _MAX_LOSSLESS or x < -_MAX_LOSSLESS else x for x in return_value]
        return jsonify({"replies": replies})

    except ZeroDivisionError as e:
        # https://cloud.google.com/bigquery/docs/remote-functions#http_response_code
        # https://cloud.google.com/bigquery/docs/remote-functions#output_format
        # aqui hay que generar el repsonse con el errorMessage
        # esto esta mal porque siempre da 400
        logging.debug("Request Headers {}".format(request.headers))
        return jsonify({"errorMessage": f"Some unhandled problem: {repr(e)}"}), 500


# Your endpoint should return the HTTP response code 200 for a successful response.
# When BigQuery receives any other value, BigQuery considers the response as a failure,
# and retries when the HTTP response code is 408, 429, 500, 503 or 504 until some internal limit.
#
# if __name__ == "__main__":
#    pass
# elif __name__ == "__test__":
#    pass
# else:
#    import google.cloud.logging
#
#    _client = google.cloud.logging.Client()
#    _client.setup_logging(log_level=logging.DEBUG)
#
