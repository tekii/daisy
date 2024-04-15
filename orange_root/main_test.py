import json
from typing import Any

# from urllib import request
# import base64

# from typing import Any
import pathlib
import pytest

# from flask import
# import pretend


# @pytest.fixture(autouse=True)
# def mock_secrets(monkeypatch):
#    from main import DAISY_SUBJECT_ACCOUNTS
#
#    monkeypatch.setenv(DAISY_SUBJECT_ACCOUNTS, "PR@legacy.tekii.com.ar;QUEUE@margot.tekii.com.ar")


# @pytest.fixture(autouse=True)
# def disable_validate_chat_authorization(monkeypatch):
#    monkeypatch.setattr(helpers.auth, "validate_chat_authorization", lambda request, audience: (None))

_TEST_AGENT_GLN = "glnws"


@pytest.fixture(autouse=True)
def set_agent_credentials(monkeypatch):
    _credentials = json.dumps({_TEST_AGENT_GLN: {"user": "pruebasws", "pass": "Clave1234"}})
    monkeypatch.setenv("AGENT_CREDENTIALS", _credentials)


@pytest.fixture
def client():
    from functions_framework import create_app

    source = pathlib.Path(__file__).resolve().parent / "main.py"
    target = "the_function"
    _app = create_app(target, source, "http")
    _app.testing = True
    return _app.test_client()


@pytest.fixture
def post_method():
    from functions_framework import create_app

    _source = pathlib.Path(__file__).resolve().parent / "main.py"
    _app = create_app("the_function", _source, "http")
    _app.testing = True
    _client = _app.test_client()

    def _the_post_method(**kw: Any):
        return _client.post(
            "/",
            # data=json.dumps(getTNC_DATA),
            content_type="application/json",
            **kw
        )
        pass

    return _the_post_method


@pytest.fixture
def C_01():
    return {"calls": [[None, 1, "", "abc"], ["abc", "9007199254740993", None, None]]}


@pytest.fixture
def REQUEST_01(C_01):
    return {
        "requestId": "124ab1c",
        "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
        "sessionUser": "test-user@test-company.com",
        "userDefinedContext": {"key1": "value1", "key2": "v2"},
        "calls": [[None, 1, "", "abc"], ["abc", "9007199254740993", None, None]],
    }


@pytest.fixture
def getTNC_UDC():
    return {"operation": "getTransaccionesNoConfirmadas"}


@pytest.fixture
def getTNC_CALLS_00():
    return [
        [_TEST_AGENT_GLN, "b", None, "2024-02-02"],
        [_TEST_AGENT_GLN, "b", 2, "2024-02-02"],
        [_TEST_AGENT_GLN, "b", 2, "2024-02-02"],
    ]


@pytest.fixture
def getTNC_DATA(getTNC_UDC, getTNC_CALLS_00):
    """getTransaccionesNoConfirmadas MOCK DATA"""
    return {
        "requestId": "124ab1c",
        "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
        "sessionUser": "test-user@test-company.com",
        "userDefinedContext": getTNC_UDC,
        "calls": getTNC_CALLS_00,
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
                "userDefinedContext": {"key1": "value1", "key2": "v2"},
                "calls": [[None, 1, "", "abc"], ["abc", "9007199254740993", None, None]],
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data == b'{"text":"Thanks for adding me to a DM, Human One!"}\n'


def test_02(post_method, getTNC_DATA):
    response = post_method(data=json.dumps(getTNC_DATA))
    assert response.status_code == 200
    assert response.data == b'{"replies":[[null,1,2,"tree"],[null,1,2,"tree"],[null,1,2,"tree"]]}\n'
    assert json.dumps(json.loads(response.data), sort_keys=True) == json.dumps(
        json.loads(b'{"replies":[[null,1,2,"tree"],[null,1,2,"tree"],[null,1,2,"tree"]]}\n'),
        sort_keys=True,
    )


def test_http_401_from_undefined_agent_credential(post_method, getTNC_DATA, monkeypatch):
    # deletes the test credentials
    import main

    monkeypatch.setattr(main, "_AGENT_CREDENTIALS", None)
    response = post_method(data=json.dumps(getTNC_DATA))
    assert response.status_code == 401


def test_http_401_from_unauthorized_agent_credential(post_method, getTNC_DATA, monkeypatch):
    # put some different credential
    import main

    monkeypatch.setattr(
        main, "_AGENT_CREDENTIALS", {"0000": {"user": "pruebasws", "pass": "Clave1234"}}
    )
    response = post_method(data=json.dumps(getTNC_DATA))
    assert response.status_code == 401


def test_http_401_from_trazmed_webservice(client, getTNC_DATA, monkeypatch):
    pass
