from adapter import TheService, OperationAdapter
from adapter.get_transacciones_no_confirmadas_adapter import _GetTransaccionesNoConfirmadasAdapter


def test_get_tnc_error_page_too_big_mock(
    entrenamiento_credentials, testing_service: type[TheService]
):
    adapter = testing_service.get_adapter("GET_TRANSACCIONES_NO_CONFIRMADAS", True)
    assert isinstance(adapter, OperationAdapter)
    assert isinstance(adapter, _GetTransaccionesNoConfirmadasAdapter)
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
        None,
        None,
        None,
        1,
        100,
    ]
    r = adapter(*all_null_args, agent_credentials=entrenamiento_credentials)
    pass


# TODO not sure what this test test...
def test_get_tnc_error_page_too_big(entrenamiento_credentials, testing_service: type[TheService]):
    adapter = testing_service.get_adapter("GET_TRANSACCIONES_NO_CONFIRMADAS", False)
    assert isinstance(adapter, OperationAdapter)
    assert isinstance(adapter, _GetTransaccionesNoConfirmadasAdapter)
    all_null_args = [
        None,
        None,
        None,
        None,
        "glnws",
        None,
        None,
        # None,
        # None,
        "2024-01-01",
        "2024-02-01",
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
        10,
    ]
    r = adapter(*all_null_args, agent_credentials=entrenamiento_credentials)
    pass
