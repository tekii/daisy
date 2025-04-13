#
import typing as t
import logging
from contextvars import ContextVar
from werkzeug.local import LocalProxy, Local


class Event:
    def __init__(self):
        pass


# _event: t.Union[Local, ContextVar[None]] = ContextVar("event", default=None)
_event: ContextVar[t.Mapping[str, t.Callable]] = ContextVar("event")
# event = LocalProxy(_event)
# event = Local(_event)


def do_dummy():
    pass


def do_added_to_space():
    logging.info("Bot added to a space")
    event = _event.get()
    # Case 1: The bot was added to a room
    if event["space"]["type"] == "ROOM":
        text = 'Thanks for adding me to "%s"!' % str(event["space"])  # ["displayName"]
    # Case 2: The bot was added to a DM
    elif event["space"]["type"] == "DM":
        text = "Thanks for adding me to a DM, %s!" % event["user"]["displayName"]

    return text


def do_removed_from_space():
    logging.info("Bot removed from a space")


def do_message():
    event = _event.get()
    text = 'Your message: "%s"' % event["message"]["text"]
    return text


_event_dispatch_table: dict[str, t.Callable] = {
    "ADDED_TO_SPACE": do_added_to_space,
    "REMOVED_FROM_SPACE": do_removed_from_space,
    "MESSAGE": do_message,
}


def do_event(event):

    # _event.set(event)

    e = _event.get()
    type = e["type"]

    handler = _event_dispatch_table.get(type)

    return handler()
