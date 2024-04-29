import json
import logging
import pathlib
import pytest
import importlib


@pytest.fixture(autouse=True)
def mock_environment(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https%3A%2F%2Fservicios.pami.org.ar%2Ftrazamed.WebService")
    monkeypatch.setenv("CONNECT_TIMEOUT", "30")
    monkeypatch.setenv("READ_TIMEOUT", "1800")


@pytest.fixture(autouse=True, name="TEST_AGENT")
def fake_agent():
    return "glnws"


@pytest.fixture
def post_method(monkeypatch, TEST_AGENT):
    # pylint: disable=C0415
    from functions_framework import create_app

    _source = pathlib.Path(__file__).resolve().parent / "main.py"
    _app = create_app("the_function", _source, "http")

    # this controls if the exceptions propagate to the test or are handled by the subject and return http 500.
    _app.testing = True
    _client = _app.test_client()

    # this is a hack until i found how to acces the loaded module from the app,
    # its important to avoid the module to load twice and override the patch
    #import main
    #
    #monkeypatch.setattr(
    #    main,
    #    "recover_agent_credentials",
    #    lambda: {TEST_AGENT: {"user": "pruebasws", "password": "Clave1234"}},
    #)

    yield lambda **kw: _client.post("/", content_type="application/json", **kw)


@pytest.fixture(name="MOCK_SINGLE_CALL")
def mock_single_call(TEST_AGENT):
    return [
        TEST_AGENT,
        1,
        "0000000000000",
        "0000000000000",
        "0000000000000",
        0,
        "2024-12-31",
        "2024-12-31",
        "2024-12-31T23:59-03:00",
        "2024-12-31T23:59",
        "2024-12-31",
        "2024-12-31",
        "R002300000000",
        "R002300000001",
        1,
        1,
        10,
        True,
    ]


@pytest.fixture(name="DUMMY_TWO_CALLS")
def call_02(TEST_AGENT):
    return [[TEST_AGENT, 1], [TEST_AGENT, 1]]


@pytest.fixture(name="MOCK_SINGLE_CALL_REQUEST")
def mock_single_call_request(MOCK_SINGLE_CALL):
    return {
        "requestId": "124ab1c",
        "caller": "//dummy.example.com/projects/dummy/jobs/dummy:US.dummy_id",
        "sessionUser": "test-user@test-company.com",
        "userDefinedContext": {"soap_operation": "GET_TRANSACCIONES", "mock_data": ""},
        "calls": [MOCK_SINGLE_CALL],
    }


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


@pytest.mark.bad_request
def test_request_user_defined_context_is_missing(post_method, MOCK_SINGLE_CALL_REQUEST):
    del MOCK_SINGLE_CALL_REQUEST["userDefinedContext"]
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 400
    assert response.data == b'{"errorMessage":"Missing key \'userDefinedContext\' accesing userDefinedContext."}\n'


@pytest.mark.bad_request
def test_request_calls_is_missing(post_method, MOCK_SINGLE_CALL_REQUEST):
    del MOCK_SINGLE_CALL_REQUEST["calls"]
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 400
    assert response.data == b'{"errorMessage":"Missing UDC calls key in the request."}\n'


@pytest.mark.bad_request
def test_invalid_timestamp_isoformat(post_method, MOCK_SINGLE_CALL_REQUEST, caplog):
    caplog.set_level(logging.ERROR)
    MOCK_SINGLE_CALL_REQUEST["calls"][0][8] = "2024-12-31T23:59Z03:00"
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 400
    assert len(caplog.records) == 1
    assert caplog.records.pop().levelname == "ERROR"
    # assert response.data == b'{"errorMessage":"Unauthorized or Undefined credentials for agent: 0000000000001"}\n'


@pytest.mark.agent_credentials
def test_unauthorized_agent(post_method, MOCK_SINGLE_CALL_REQUEST):
    MOCK_SINGLE_CALL_REQUEST["calls"][0][0] = "0000000000001"
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 401
    assert response.data == b'{"errorMessage":"Unauthorized credentials for agent: 0000000000001"}\n'


@pytest.mark.mock_data
def test_mock_dateset_some(post_method, MOCK_SINGLE_CALL_REQUEST):
    # MOCK_SINGLE_CALL_REQUEST["userDefinedContext"]["mock_data"] = ""
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 200


@pytest.mark.mock_data
def test_mock_dateset_single_call_single_page(post_method, MOCK_SINGLE_CALL_REQUEST):
    # MOCK_SINGLE_CALL_REQUEST["userDefinedContext"]["mock_data"] = ""
    MOCK_SINGLE_CALL_REQUEST["calls"][0][15] = 1
    MOCK_SINGLE_CALL_REQUEST["calls"][0][16] = 50
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "replies" in data
    replies = data["replies"]
    assert len(replies) == 1
    reply = replies[0]
    assert len(reply) == 100  # the api ignores page_max


@pytest.mark.mock_data
def test_mock_dateset_10_calls_all_pages(post_method, MOCK_SINGLE_CALL, MOCK_SINGLE_CALL_REQUEST):
    # MOCK_SINGLE_CALL_REQUEST["userDefinedContext"]["mock_data"] = ""
    # MOCK_SINGLE_CALL_REQUEST["calls"][0][16] = 50
    for page in range(2, 6):
        extra_call = MOCK_SINGLE_CALL.copy()
        extra_call[15] = page
        # extra_call[16] = 50
        MOCK_SINGLE_CALL_REQUEST["calls"].append(extra_call)
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "replies" in data
    replies = data["replies"]
    # 460 rows
    assert len(replies) == 5
    assert len(replies.pop()) == 60
    for reply in replies:
        assert len(reply) == 100


@pytest.mark.mock_data
def test_mock_dateset_single_call_no_result(post_method, MOCK_SINGLE_CALL_REQUEST):
    MOCK_SINGLE_CALL_REQUEST["userDefinedContext"]["mock_data"] = ""
    MOCK_SINGLE_CALL_REQUEST["calls"][0][15] = 11
    MOCK_SINGLE_CALL_REQUEST["calls"][0][16] = 50
    response = post_method(data=json.dumps(MOCK_SINGLE_CALL_REQUEST))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "replies" in data
    replies = data["replies"]
    assert len(replies) == 1
    reply = replies[0]
    # need to decide if the right empty result is None or []
    assert reply is None


@pytest.mark.environment_undefined
def test_environment_undefined_connect_timeout(monkeypatch):
    monkeypatch.delenv("CONNECT_TIMEOUT")
    mod = importlib.import_module("marshals.marshals")
    with pytest.raises(SystemExit) as e:
        importlib.reload(mod)
    assert e.type == SystemExit


@pytest.mark.environment_undefined
def test_environment_undefined_read_timeout(monkeypatch):
    monkeypatch.delenv("READ_TIMEOUT")
    mod = importlib.import_module("marshals.marshals")
    with pytest.raises(SystemExit) as e:
        importlib.reload(mod)
    assert e.type == SystemExit


@pytest.mark.environment_undefined
def test_environment_undefined_target_url(monkeypatch):
    monkeypatch.delenv("TARGET_URL")
    mod = importlib.import_module("marshals.marshals")
    with pytest.raises(SystemExit) as e:
        importlib.reload(mod)
    assert e.type == SystemExit
