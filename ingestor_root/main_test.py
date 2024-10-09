import json
import base64
import pathlib
import pytest

from typing import Any
from cloudevents.http import CloudEvent  # , to_structured
from cloudevents.conversion import to_structured
from functions_framework import create_app


# import pretend
@pytest.fixture(autouse=True)
def mock_secrets(ingestor_queue_service_account_credentials, monkeypatch):
    # the first fixture is ingestor_queue_service_account_credentials before importing main below
    from main import DAISY_SUBJECT_ACCOUNTS

    monkeypatch.setenv(DAISY_SUBJECT_ACCOUNTS, "PR@legacy.tekii.com.ar;QUEUE@margot.tekii.com.ar;queue@margot.tekii.com.ar")


@pytest.fixture
def client():
    source = pathlib.Path(__file__).resolve().parent / "main.py"
    target = "the_function"
    _app = create_app(target, source, "cloudevent")
    # _app.testing = True
    return _app.test_client()


def message_encode_helper(payload: Any) -> str:
    data1 = json.dumps(payload)
    data2 = data1.encode("utf-8")
    data3 = base64.b64encode(data2)
    data4 = data3.decode("utf-8")
    return data4


@pytest.fixture
def mock_ce():
    attributes = {
        #'specversion': '1.0',
        #'id': '4707084296741162',
        "source": "//pubsub.googleapis.com/projects/daisy-dev01/topics/ingestor-queue",
        "type": "google.cloud.pubsub.topic.v1.messagePublished",
        #'datacontenttype': 'application/json',
        #'time': '2022-07-18T23:07:39.111Z'
    }
    data = {
        "message": {
            # https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
            "data": "eyJlbWFpbEFkZHJlc3MiOiJwckBsZWdhY3kudGVraWkuY29tLmFyIiwiaGlzdG9yeUlkIjoxMzYxNzAwMH0=",
            # "messageId": "4707084296741162",
            # "message_id": "4707084296741162",
            # "publishTime": "2022-07-18T23:07:39.111Z",
            # "publish_time": "2022-07-18T23:07:39.111Z",
        },
        # "subscription": "projects/daisy-dev01/subscriptions/eventarc-us-central1-function-5-637946-sub-190",
    }
    return CloudEvent(attributes=attributes, data=data)


def test_04(capsys, mock_ce):
    from main import the_function

    # event = type('cloudevent', (object,), {"attributes": {}, "data": {}})
    event = mock_ce
    the_function(event)
    out, err = capsys.readouterr()
    pass
    # assert "pr@legacy.tekii.com.ar\n13617000\n" == out


def test_02(capsys, mock_ce):
    from main import the_function

    event = mock_ce
    event.data["message"]["data"] = message_encode_helper(payload={"emailAddress": "pr@legacy.tekii.com.ar", "historyId": "13617000"})
    the_function(event)
    out, _ = capsys.readouterr()
    # assert "pr@legacy.tekii.com.ar\n13617000\n" == out


def test_00(client, mock_ce):
    ce = mock_ce
    headers, data = to_structured(ce)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 200
    assert response.data == b"OK"


def test_01(client, mock_ce):
    ce = mock_ce
    ce._attributes["type"] = "wrong-type"
    headers, data = to_structured(ce)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 500
    assert response.data == b"500 Internal Server Error: NOT the cloud_event type expected: wrong-type"


# def test_05(capsys, mock_ce, monkeypatch):
#    import main
#
#    monkeypatch.delenv(main.DAISY_SUBJECT_ACCOUNTS)
#    main.the_function(mock_ce)
#    out, _ = capsys.readouterr()
#    assert "pr@legacy.tekii.com.ar\n13617000\n" == out


def test_07(client, mock_ce, monkeypatch):
    from main import DAISY_SUBJECT_ACCOUNTS

    monkeypatch.delenv(DAISY_SUBJECT_ACCOUNTS)

    headers, data = to_structured(mock_ce)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 500
    assert response.data == b"500 Internal Server Error: DAISY_SUBJECT_ACCOUNTS is not set or its empty."


def test_08(client, mock_ce, monkeypatch):
    from main import DAISY_SUBJECT_ACCOUNTS

    monkeypatch.setenv(DAISY_SUBJECT_ACCOUNTS, "")

    headers, data = to_structured(mock_ce)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 500
    assert response.data == b"500 Internal Server Error: DAISY_SUBJECT_ACCOUNTS is not set or its empty."


def test_09(client, mock_ce):
    ce = mock_ce
    del ce.data["message"]["data"]

    headers, data = to_structured(ce)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 500
    assert response.data == b"500 Internal Server Error: Exception decoding PubSub message: KeyError('data')"


def test_19(client, mock_ce):
    ce = mock_ce
    ce.data["message"]["data"] = message_encode_helper({"emailAddress": "queue@margot.tekii.com.ar", "historyId": "4255018"})

    headers, data = to_structured(ce)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 500
    assert response.data == b"500 Internal Server Error: 'subject' is not in DAISY_SUBJECT_ACCOUNTS."
