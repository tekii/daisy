import functions_framework
from flask import abort, jsonify

#_PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER", "952137789881")

# Max INT64 value encoded as a number in JSON by TO_JSON_STRING. Larger values are encoded as
# strings.
# See https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
_MAX_LOSSLESS=9007199254740992


@functions_framework.http
def the_function(request):
    """ """
    try:
        return_value = []
        request_json = request.get_json()
        
        calls = request_json['calls']
        for call in calls:
            return_value.append(sum([int(x) if isinstance(x, str) else x for x in call if x is not None]))

        replies = [str(x) if x > _MAX_LOSSLESS or x < -_MAX_LOSSLESS else x for x in return_value]
        return jsonify( { "replies" :  replies } )

    except Exception as e:
        abort(400, description=(f"Some problem: {repr(e)}"))
