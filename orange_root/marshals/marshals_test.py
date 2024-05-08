import pytest
from .marshals import *

@pytest.fixture(autouse=False)
def test_environment(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https%3A%2F%2Fservicios.pami.org.ar%2Ftrazamed.WebService")
    monkeypatch.setenv("CONNECT_TIMEOUT", "30")
    monkeypatch.setenv("READ_TIMEOUT", "1800")
    # seems to be that isinstance doesnt works because the multiple import paths...
    #mod = importlib.import_module("marshals","..marshals")
#    from .marshals import TheMarshallers 
    #from .marshals import TheMarshallers
    TheService().configure_or_die()
    yield #TheMarshallers
    #tm = TheService()
    #tm._is_already_configured = False
    #tm._marshals = {}



@pytest.fixture(name="the_agent_credentials")
def agent_credentials():
    return {"user": "pruebasws", "password": "Clave1234"}


@pytest.fixture()  # name="THE_ARGS")
def complete_args():
    return [
        "0000000000000",
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
        100,
        True,
    ]


def test_get_transacciones_args_full(complete_args, the_agent_credentials, test_environment):
    operation = "GET_TRANSACCIONES"
    the_marshal = test_environment.get_marshal(operation)
    #assert isinstance(the_marshal, test_environment.marshals.Marshal)
    #assert isinstance(the_marshal, test_environment.marshals._GetTransacciones)
    _ = the_marshal(*complete_args, agent_credentials=the_agent_credentials, mock_data=True)
    pass


@pytest.mark.bad_request
@pytest.mark.marshal_error
def test_get_transacciones_args_invalid_isoformat(complete_args, the_agent_credentials, test_environment):
    operation = "GET_TRANSACCIONES"
    the_marshal = test_environment.get_marshal(operation)
    #assert isinstance(the_marshal, test_environment.Marshal)
    #assert isinstance(the_marshal, test_environment._GetTransacciones)
    invalid = complete_args
    invalid[8] = "2024-12-31T23:59Z03:00"
    with pytest.raises(test_environment.MarshalError) as e_info:
        _ = the_marshal(*complete_args, agent_credentials=the_agent_credentials, mock_data=True)
    pass


def test_get_transacciones_args_all_nulls(the_agent_credentials, test_environment):
    adapter = TheService().get_adapter("GET_TRANSACCIONES")
    #the_marshal = test_environment.get_marshal(operation)
    assert isinstance(adapter, OperationAdapter)
    #assert isinstance(the_marshal, test_environment._GetTransacciones)
    all_null_args = [
        "0000000000000",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        1,
        100,
        True,
    ]
    r = adapter(*all_null_args, agent_credentials=the_agent_credentials, mock_data=True)
    pass


def test_marshalship_singleton(test_environment):
    
    there_can_be_only_one = TheService()
    pass
    there_can_be_only_one_ = TheService()
    pass
    there_can_be_only_one.configure()
    pass
    adapter = there_can_be_only_one.get_adapter("GET_TRANSACCIONES")
    pass
