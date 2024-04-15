import os
import json

# from urllib import response
import functions_framework
from flask import jsonify, abort

from trazamed import getRelay

_AGENT_CREDENTIALS = json.loads(os.environ.get("AGENT_CREDENTIALS"))


@functions_framework.errorhandler(ZeroDivisionError)
def handle_zero_division(e):
    return "I'm a teapot", 418


@functions_framework.errorhandler(401)
def handle_401(e):
    # aqui puede manejar si reitenta o aborta
    return jsonify({"errorMessage": f"AGENT problem: {repr(e)}"}), 401


@functions_framework.http
def the_function(request):
    """ """
    try:
        request_json = request.get_json()

        try:
            operation = request_json["userDefinedContext"]["operation"]
            calls = request_json["calls"]
        except KeyError as e:
            return jsonify({"errorMessage": f"BAD REQUEST problem: {repr(e)}"}), 400

        # if _AGENT_CREDENTIALS is None:
        #    abort(401,"_AGENT_CREDENTIALS is None")

        # relay = getRelay(operation)
        replies = []

        for call_args in calls:

            agent = call_args[0]

            agent_credentials = _AGENT_CREDENTIALS.get(agent)
            if agent_credentials is None:
                abort(401, "Unauthorized agent")

            r = relay(agent_credentials, call_args)
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
        return jsonify({"errorMessage": f"Some unhandled problem: {repr(e)}"}), 500


# Your endpoint should return the HTTP response code 200 for a successful response.
# When BigQuery receives any other value, BigQuery considers the response as a failure,
# and retries when the HTTP response code is 408, 429, 500, 503 or 504 until some internal limit.
