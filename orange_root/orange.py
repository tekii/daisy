import os
import logging

# from contextvars import ContextVar
# from werkzeug.local import LocalProxy
from flask import Flask, request, abort, jsonify

# _some_var = ContextVar("some_var", default=1)
# some_var = LocalProxy(_some_var)


_PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER", "952137789881")

# Max INT64 value encoded as a number in JSON by TO_JSON_STRING. Larger values are encoded as
# strings.
# See https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
_MAX_LOSSLESS=9007199254740992

app = Flask(__name__)

#@app.error_processor
#def my_auth_error_processor(error):
#    body = {
#        'error_message': error.message,
#        'error_detail': error.detail,
#        'status_code': error.status_code
#    }
#    return body, error.status_code, error.headers

@app.errorhandler(401)
def unauthorized(e):
    error = str(e)
    logging.debug(error)
    return jsonify(error=error), 401


@app.route("/", methods=['POST'])
def batch_add():
    """ """
    try:
        return_value = []
        request_json = request.get_json()
        calls = request_json['calls']
        print(calls)
        for call in calls:
            print(call)
            return_value.append(sum([int(x) if isinstance(x, str) else x for x in call if x is not None]))

        replies = [str(x) if x > _MAX_LOSSLESS or x < -_MAX_LOSSLESS else x for x in return_value]
        return jsonify( { "replies" :  replies } )

    except Exception as e:
        return jsonify( { "errorMessage": str(e) } ), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

elif __name__ == "__test__":
    pass

else:
    import google.cloud.logging

    _client = google.cloud.logging.Client()
    _client.setup_logging(log_level=logging.DEBUG)
