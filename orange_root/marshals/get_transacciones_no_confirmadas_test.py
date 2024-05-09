import pytest
from .adapter import *
from .get_transacciones_no_confirmadas_adapter import *

def test_get_tnc_error_page_too_big(entrenamiento_credentials, testing_service:type[TheService]):
    adapter = testing_service.get_adapter("GET_TRANSACCIONES_NO_CONFIRMADAS")
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
        1,
        #        100,
        #        True,
    ]
    r = adapter(*all_null_args, agent_credentials=entrenamiento_credentials, mock_data=True)
    pass