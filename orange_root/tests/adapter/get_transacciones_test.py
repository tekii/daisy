import pytest

from adapter import OperationAdapter, TheService, AdapterError
from adapter.get_transacciones_adapter import _GetTransaccionesAdapter


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


def test_get_transacciones_args_full(
    complete_args, entrenamiento_credentials, testing_service: type[TheService]
):
    operation = "GET_TRANSACCIONES"
    adapter = testing_service.get_adapter(operation, True)
    assert isinstance(adapter, OperationAdapter)
    assert isinstance(adapter, _GetTransaccionesAdapter)
    _ = adapter(*complete_args, agent_credentials=entrenamiento_credentials)
    pass


@pytest.mark.bad_request
@pytest.mark.marshal_error
def test_get_transacciones_args_invalid_isoformat(
    complete_args, entrenamiento_credentials, testing_service: type[TheService]
):
    operation = "GET_TRANSACCIONES"
    adapter = testing_service.get_adapter(operation, True)
    assert isinstance(adapter, OperationAdapter)
    assert isinstance(adapter, _GetTransaccionesAdapter)
    invalid = complete_args
    invalid[8] = "2024-12-31T23:59Z03:00"
    with pytest.raises(AdapterError) as e_info:
        _ = adapter(*complete_args, agent_credentials=entrenamiento_credentials)
    pass


def test_get_transacciones_args_all_nulls(
    entrenamiento_credentials, testing_service: type[TheService]
):
    adapter = TheService().get_adapter("GET_TRANSACCIONES", True)
    assert isinstance(adapter, OperationAdapter)
    assert isinstance(adapter, _GetTransaccionesAdapter)
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
    r = adapter(*all_null_args, agent_credentials=entrenamiento_credentials)
    pass


def test_marshalship_singleton(testing_service: type[TheService]):
    there_can_be_only_one = TheService()
    assert there_can_be_only_one is testing_service
    assert there_can_be_only_one is testing_service.configure_or_die()
    # adapter = there_can_be_only_one.get_adapter("GET_TRANSACCIONES")
    pass
