import json

# from urllib import request
# import base64

# from typing import Any
import pathlib
import pytest

# import pretend


# @pytest.fixture(autouse=True)
# def mock_secrets(monkeypatch):
#    from main import DAISY_SUBJECT_ACCOUNTS
#
#    monkeypatch.setenv(DAISY_SUBJECT_ACCOUNTS, "PR@legacy.tekii.com.ar;QUEUE@margot.tekii.com.ar")


@pytest.fixture(autouse=True, name="TEST_AGENT")
def fake_agent():
    return "glnws"


# @pytest.fixture  # (autouse=True)
# def recover_agent_gredentials_patched(monkeypatch, TEST_AGENT):
#    # pylint: disable=C0415
#    # import main
#
#    monkeypatch.setattr(
#        main,
#        "recover_agent_gredentials",
#        lambda: {TEST_AGENT: {"user": "pruebasws", "pass": "Clave1234"}},
#    )


# @pytest.fixture
# def client():
#    pylint: disable=C0415
# from functions_framework import create_app
#
# source = pathlib.Path(__file__).resolve().parent / "main.py"
# target = "the_function"
# _app = create_app(target, source, "http")
# _app.testing = True
# return _app.test_client()


@pytest.fixture
def post_method():  # monkeypatch, TEST_AGENT):
    # pylint: disable=C0415
    from functions_framework import create_app

    _source = pathlib.Path(__file__).resolve().parent / "main.py"
    _app = create_app("the_function", _source, "http")

    # this controls if the exceptions propagate to the test or are handled by the subject and return http 500.
    _app.testing = True
    _client = _app.test_client()

    # monkeypatch.setattr(
    #    ,
    #    "recover_agent_gredentials",
    #    lambda: {TEST_AGENT: {"user": "pruebasws", "pass": "Clave1234"}},
    # )

    return lambda **kw: _client.post("/", content_type="application/json", **kw)


@pytest.fixture(name="DUMMY_ONE_CALL")
def call_01(TEST_AGENT):
    return [[TEST_AGENT, 1]]


@pytest.fixture(name="DUMMY_TWO_CALLS")
def call_02(TEST_AGENT):
    return [[TEST_AGENT, 1], [TEST_AGENT, 1]]


@pytest.fixture(name="DUMMY_REQUEST")
def dummy_request_a(DUMMY_ONE_CALL):
    return {
        "requestId": "124ab1c",
        "caller": "//dummy.example.com/projects/dummy/jobs/dummy:US.dummy_id",
        "sessionUser": "test-user@test-company.com",
        "userDefinedContext": {"soap_operation": "getTransaccionesWS"},
        "calls": DUMMY_ONE_CALL,
    }


@pytest.fixture(name="TNC_UDC")
def get_tnc_udc():
    return {"operation": "getTransaccionesWS", "mode": "mock"}


@pytest.fixture(name="TNC_CALLS_00")
def get_tnc_calls_00(TEST_AGENT):
    return [
        [TEST_AGENT, 1, None, "2024-02-02"],
        [TEST_AGENT, 2, 2, "2024-02-02"],
        [TEST_AGENT, 3, 2, "2024-02-02"],
    ]


@pytest.fixture(name="TNC_DATA")
def get_tnc_data(TNC_UDC, DUMMY_ONE_CALL):
    return {
        "requestId": "124ab1c",
        "caller": "//dummy.example.com/projects/dummy/jobs/dummy:US.dummy_id",
        "sessionUser": "test-user@test-company.com",
        "userDefinedContext": TNC_UDC,
        "calls": DUMMY_ONE_CALL,
    }


#
#
#


# def test_02(post_method, TNC_DATA):
#    response = post_method(data=json.dumps(TNC_DATA))
#    assert response.status_code == 200
#    assert response.data == b'{"replies":[[null,1,2,"tree"],[null,1,2,"tree"],[null,1,2,"tree"]]}\n'
#    assert json.dumps(json.loads(response.data), sort_keys=True) == json.dumps(
#        json.loads(b'{"replies":[[null,1,2,"tree"],[null,1,2,"tree"],[null,1,2,"tree"]]}\n'),
#        sort_keys=True,
#    )


# @pytest.mark.secret_credentials
# def test_http_401_from_undefined_agent_credential(post_method, TNC_DATA, monkeypatch):
#    # pylint: disable=C0415
#    # import main
#
#    monkeypatch.setattr(main, "_AGENT_CREDENTIALS", None)
#    response = post_method(data=json.dumps(TNC_DATA))
#    assert response.status_code == 401


# @pytest.mark.secret_credentials
# def test_http_401_from_unauthorized_agent_credential(post_method, TNC_DATA, monkeypatch):
#    # put some different credential
#    # pylint: disable=C0415
#    import main
#
#    monkeypatch.setattr(
#        main,
#        "recover_agent_gredentials",
#        lambda: {"glnws": {"user": "pruebasws", "pass": "---------"}},
#    )
#
#    response = post_method(data=json.dumps(TNC_DATA))
#    assert response.status_code == 401


## pylint: disable=W0613
# def test_http_401_from_trazmed_webservice(post_method, TNC_DATA, monkeypatch):
#    pass


@pytest.mark.bad_request
def test_request_user_defined_context_is_missing(post_method, DUMMY_REQUEST):
    del DUMMY_REQUEST["userDefinedContext"]
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 400
    assert response.data == b'{"errorMessage":"Missing key \'userDefinedContext\' accesing userDefinedContext."}\n'


@pytest.mark.bad_request
def test_request_calls_is_missing(post_method, DUMMY_REQUEST):
    del DUMMY_REQUEST["calls"]
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 400
    assert response.data == b'{"errorMessage":"Missing [calls]."}\n'


@pytest.mark.agent_credentials
def test_unauthorized_agent(post_method, DUMMY_REQUEST):
    DUMMY_REQUEST["calls"][0][0] = "0000000000001"
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 401
    assert response.data == b'{"errorMessage":"Unauthorized agent: 0000000000001"}\n'


@pytest.mark.mock_dataset
def test_mock_dateset_some(post_method, DUMMY_REQUEST):
    DUMMY_REQUEST["userDefinedContext"]["mock_dataset"] = ""
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 200


@pytest.mark.mock_dataset
def test_mock_dateset_single_call_single_page(post_method, DUMMY_REQUEST):
    DUMMY_REQUEST["userDefinedContext"]["mock_dataset"] = ""
    DUMMY_REQUEST["calls"][0][1] = 1
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "replies" in data
    replies = data["replies"]
    assert len(replies) == 1
    reply = replies[0]
    assert len(reply) == 50


@pytest.mark.mock_dataset
def test_mock_dateset_10_calls_all_pages(post_method, DUMMY_REQUEST):
    DUMMY_REQUEST["userDefinedContext"]["mock_dataset"] = ""
    DUMMY_REQUEST["calls"] = []
    for page in range(1, 11):
        DUMMY_REQUEST["calls"].append(["glnws", page])
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "replies" in data
    replies = data["replies"]
    # 460 rows
    assert len(replies) == 10
    assert len(replies.pop()) == 10
    for reply in replies:
        assert len(reply) == 50


@pytest.mark.mock_dataset
def test_mock_dateset_single_call_no_result(post_method, DUMMY_REQUEST):
    DUMMY_REQUEST["userDefinedContext"]["mock_dataset"] = ""
    DUMMY_REQUEST["calls"][0][1] = 11
    response = post_method(data=json.dumps(DUMMY_REQUEST))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "replies" in data
    replies = data["replies"]
    assert len(replies) == 1
    reply = replies[0]
    assert reply is None
