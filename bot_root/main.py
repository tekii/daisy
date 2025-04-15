import os
import logging

# from contextvars import ContextVar
# from werkzeug.local import LocalProxy
from flask import Flask, request, render_template, abort, jsonify  # type: ignore

# _some_var = ContextVar("some_var", default=1)
# some_var = LocalProxy(_some_var)

from helpers.auth import validate_chat_authorization
from chat import _event as chat_event, do_event

_PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER", "952137789881")

app = Flask(__name__)


@app.errorhandler(401)
def unauthorized(e):
    error = str(e)
    logging.debug(error)
    return jsonify(error=error), 401


@app.route("/", methods=["POST"])
def home_post():
    """ """

    validate_chat_authorization(request=request, audience=_PROJECT_NUMBER)

    logging.debug("Request Headers: {}".format(request.headers))
    # logging.debug("{}".format(request.__dict__))

    event = request.get_json()
    # logging.debug(f"Event: {str(event)}")

    chat_event.set(event)

    resp = None
    text = ""

    text = do_event(chat_event)

    # if event["type"] == "REMOVED_FROM_SPACE":
    #    logging.info("Bot removed from a space")
    #
    ## Case 1: The bot was added to a room
    # if event["type"] == "ADDED_TO_SPACE" and event["space"]["type"] == "ROOM":
    #    text = 'Thanks for adding me to "%s"!' % str(event["space"])  # ["displayName"]
    #
    ## Case 2: The bot was added to a DM
    # elif event["type"] == "ADDED_TO_SPACE" and event["space"]["type"] == "DM":
    #    text = "Thanks for adding me to a DM, %s!" % event["user"]["displayName"]

    # if event["type"] == "MESSAGE":
    #    text = 'Your message: "%s"' % event["message"]["text"]

    # else:
    #    text = str(event)

    resp = jsonify({"text": text})

    return resp


@app.route("/", methods=["GET"])
def home_get():

    validate_chat_authorization(request=request, audience=_PROJECT_NUMBER)
    # logging.debug(f"GET {str(request.get_json())}")
    logging.debug("Request Headers {}".format(request.headers))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

elif __name__ == "__test__":
    pass

else:
    import google.cloud.logging  # type: ignore

    _client = google.cloud.logging.Client()
    _client.setup_logging(log_level=logging.DEBUG)
