from contextlib import nullcontext
import json
import base64
import pathlib
import pytest
from typing import Any

# from flask import
# import pretend


# @pytest.fixture(autouse=True)
# def mock_secrets(monkeypatch):
#    from main import DAISY_SUBJECT_ACCOUNTS
#
#    monkeypatch.setenv(DAISY_SUBJECT_ACCOUNTS, "PR@legacy.tekii.com.ar;QUEUE@margot.tekii.com.ar")


#@pytest.fixture(autouse=True)
#def disable_validate_chat_authorization(monkeypatch):
#    monkeypatch.setattr(helpers.auth, "validate_chat_authorization", lambda request, audience: (None))


@pytest.fixture
def client():
    from importlib.util import spec_from_file_location, module_from_spec

    # from importlib.machinery import SourceFileLoader
    source = pathlib.Path(__file__).resolve().parent / "orange.py"
    # spec = spec_from_loader("main", SourceFileLoader("main", str(source)))
    spec = spec_from_file_location("__test__", str(source))
    main = module_from_spec(spec)
    spec.loader.exec_module(main)
    # main = SourceFileLoader("main", str(source)).load_module()
    return main.app.test_client()


@pytest.fixture
def C_01():
    return {
        "calls" : [
            [None, 1, "", "abc"],
            ["abc", "9007199254740993", None, None]
        ]
    }

@pytest.fixture
def REQUEST_01(C_01):
    return {
        "requestId": "124ab1c",
        "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
        "sessionUser": "test-user@test-company.com",
        "userDefinedContext": {
            "key1": "value1",
            "key2": "v2"
        },
        "calls": [
            [None, 1, "", "abc"],
            ["abc", "9007199254740993", None, None]
        ]
    }


@pytest.mark.skip(reason="no way of currently testing this")
def test_01(client, REQUEST_01):
    response = client.post(
        "/",
        data=json.dumps(
            {
                "requestId": "124ab1c",
                "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
                "sessionUser": "test-user@test-company.com",
                "userDefinedContext": {
                    "key1": "value1",
                    "key2": "v2"
                },
                "calls": [
                    [None, 1, "", "abc"],
                    ["abc", "9007199254740993", None, None]
                ]
            }            
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data == b'{"text":"Thanks for adding me to a DM, Human One!"}\n'

def test_02(client, REQUEST_01):
    response = client.post(
        "/",
        data=json.dumps(
            {
                "requestId": "124ab1c",
                "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
                "sessionUser": "test-user@test-company.com",
                "userDefinedContext": {
                    "key1": "value1",
                    "key2": "v2"
                },
                "calls": [
                    [1, 1],
                    [2, 2]
                ]
            }            
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data == b'{"replies":[2,4]}\n'

