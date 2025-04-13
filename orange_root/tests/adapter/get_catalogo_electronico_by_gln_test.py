import pytest
from adapter import OperationAdapter
from . import *
from .get_catalogo_electronico_by_gln_adapter import *


def test_get_catalogo_by_gln_args_all_nulls(entrenamiento_credentials, testing_service:type[TheService]):
    adapter = TheService().get_adapter("GET_CATALOGO_ELECTRONICO_BY_GLN",False)
    assert isinstance(adapter, OperationAdapter)
    assert isinstance(adapter, _GetCatalogoElectronicoByGLNAdapter)
    all_null_args = [
        "glnws",
        None,
        None,
        None,
        None,
        None,
        200,
        100
    ]
    r = adapter(*all_null_args, agent_credentials=entrenamiento_credentials)
    pass