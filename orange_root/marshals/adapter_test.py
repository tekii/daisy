import pytest
from .adapter import *
from .get_transacciones_adapter import *


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


def test_get_transacciones_args_full(complete_args, entrenamiento_credentials, testing_service):
    operation = "GET_TRANSACCIONES"
    the_marshal = testing_service.get_marshal(operation)
    # assert isinstance(the_marshal, testing_service.marshals.Marshal)
    # assert isinstance(the_marshal, testing_service.marshals._GetTransacciones)
    _ = the_marshal(*complete_args, agent_credentials=entrenamiento_credentials, mock_data=True)
    pass


@pytest.mark.bad_request
@pytest.mark.marshal_error
def test_get_transacciones_args_invalid_isoformat(complete_args, entrenamiento_credentials, testing_service):
    operation = "GET_TRANSACCIONES"
    the_marshal = testing_service.get_marshal(operation)
    # assert isinstance(the_marshal, testing_service.Marshal)
    # assert isinstance(the_marshal, testing_service._GetTransacciones)
    invalid = complete_args
    invalid[8] = "2024-12-31T23:59Z03:00"
    with pytest.raises(testing_service.MarshalError) as e_info:
        _ = the_marshal(*complete_args, agent_credentials=entrenamiento_credentials, mock_data=True)
    pass


def test_get_transacciones_args_all_nulls(entrenamiento_credentials, testing_service):
    adapter = TheService().get_adapter("GET_TRANSACCIONES")
    assert isinstance(adapter, OperationAdapter)
    # assert isinstance(the_marshal, testing_service._GetTransacciones)
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
        #        100,
        #        True,
    ]
    r = adapter(*all_null_args, agent_credentials=entrenamiento_credentials, mock_data=True)
    pass


def test_marshalship_singleton(testing_service):

    there_can_be_only_one = TheService()
    pass
    there_can_be_only_one_ = TheService()
    pass
    there_can_be_only_one.configure_or_die()()
    pass
    adapter = there_can_be_only_one.get_adapter("GET_TRANSACCIONES")
    pass
