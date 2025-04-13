import json
import base64
import pathlib
import pytest
from typing import Any

# from flask import
# import pretend

import helpers.auth

# @pytest.fixture(autouse=True)
# def mock_secrets(monkeypatch):
#    from main import DAISY_SUBJECT_ACCOUNTS
#
#    monkeypatch.setenv(DAISY_SUBJECT_ACCOUNTS, "PR@legacy.tekii.com.ar;QUEUE@margot.tekii.com.ar")


@pytest.fixture(autouse=True)
def disable_validate_chat_authorization(monkeypatch):
    monkeypatch.setattr(helpers.auth, "validate_chat_authorization", lambda request, audience: (None))


@pytest.fixture
def client():
    from importlib.util import spec_from_file_location, module_from_spec

    # from importlib.machinery import SourceFileLoader
    source = pathlib.Path(__file__).resolve().parent / "main.py"
    # spec = spec_from_loader("main", SourceFileLoader("main", str(source)))
    spec = spec_from_file_location("__test__", str(source))
    main = module_from_spec(spec)
    spec.loader.exec_module(main)
    # main = SourceFileLoader("main", str(source)).load_module()
    return main.app.test_client()


@pytest.fixture
def HUMAN_ONE():
    return {
        "name": "users/000000000000000000001",
        "displayName": "Human One",
        "avatarUrl": "https://lh3.googleusercontent.com/avatar",
        "email": "one@example.com",
        "type": "HUMAN",
        "domainId": "example.com",
    }


@pytest.fixture
def DM_SPACE():
    return {
        "name": "spaces/75U6AEAAAAE",
        "type": "DM",
        "singleUserBotDm": True,
        "spaceThreadingState": "UNTHREADED_MESSAGES",
        "spaceType": "DIRECT_MESSAGE",
        "spaceHistoryState": "HISTORY_OFF",
    }


@pytest.fixture
def ROOM_SPACE():
    return {
        "name": "spaces/AAAAAAAAAAA",
        "type": "ROOM",
        "displayName": "THE A ROOM",
        "threaded": True,
        "spaceThreadingState": "GROUPED_MESSAGES",
        "spaceType": "SPACE",
        "spaceHistoryState": "HISTORY_ON",
    }


@pytest.fixture
def mock_MESSAGE(HUMAN_ONE, ROOM_SPACE):
    return {
        "type": "MESSAGE",
        "eventTime": "2022-08-09T00:29:34.471343Z",
        "message": {
            "name": "spaces/AAAAAAAAAAA/messages/jIhRq9fdhbQ.B7_w7lCdp58",
            "sender": HUMAN_ONE,
            "createTime": "2022-08-09T00:29:34.471343Z",
            "text": "/demo demo",
            "annotations": [
                {
                    "type": "SLASH_COMMAND",
                    "startIndex": 0,
                    "length": 5,
                    "slashCommand": {
                        "bot": {
                            "name": "users/117667521047122819027",
                            "displayName": "daisy",
                            "avatarUrl": "https://lh3.googleusercontent.com/proxy/WhX5bm6M-Lbb9xLZ6tchz3h-Wua3qqOSPLJCvpg87B16uvpHAC1PE07JaAFpw64KF8PPEXiCTIRoofQEXVEECeuB5O_eNj-La-H_NandU5yHw-EbsCpEMGIqzoZBfmaM8KFkoGsq5pXTTsPFsBMzPPUmHkHR7WKBrtIJ7cxK4pG3m7rvOJtTVdlyvEVbgyyqgAyRK99B8HDnKG3PNQ",
                            "type": "BOT",
                        },
                        "type": "INVOKE",
                        "commandName": "/demo",
                        "commandId": "101",
                    },
                }
            ],
            "thread": {"name": "spaces/AAAAiJ9w3lo/threads/jIhRq9fdhbQ", "retentionSettings": {"state": "PERMANENT"}},
            "space": ROOM_SPACE,
            "argumentText": " demo",
            "slashCommand": {"commandId": "101"},
            "retentionSettings": {"state": "PERMANENT"},
        },
        "user": HUMAN_ONE,
        "space": ROOM_SPACE,
        "configCompleteRedirectUrl": "https://chat.google.com/api/bot_config_complete?token=AArJXmRNBdGD9tAL5a7QdAvnLsROveyHYJu2BQOj0U2cFgySejda2XMf2bKlFjurUcJl_YprbcxsuQgGOMxP6Wl4GUwrNMXPOnbf1YW6HSh2ziOAdcKv2B542Y4HsnA9uVqAxb6PqRL-mgjTMpp5qsQ%3D",
    }


def test_01(client, HUMAN_ONE, DM_SPACE):
    response = client.post(
        "/",
        data=json.dumps(
            {
                "type": "ADDED_TO_SPACE",
                "eventTime": "2022-08-09T04:32:03.696908Z",
                "user": HUMAN_ONE,
                "space": DM_SPACE,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data == b'{"text":"Thanks for adding me to a DM, Human One!"}\n'


def test_02(client, HUMAN_ONE, DM_SPACE):
    test_event = {
        "type": "REMOVED_FROM_SPACE",
        "eventTime": "2022-08-07T04: 46: 23.063869Z",
        "user": HUMAN_ONE,
        "space": DM_SPACE,
    }
    response = client.post("/", data=json.dumps(test_event), content_type="application/json")
    assert response.status_code == 200
