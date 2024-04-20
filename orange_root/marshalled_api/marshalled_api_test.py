import pytest

# from marshalled_api import MARSHALS
import marshalled_api


def test_get_transacciones_args_00():
    operation = "GET_TRANSACCIONES"
    _marshal = marshalled_api.MARSHALS[operation]
    assert isinstance(_marshal, marshalled_api.Marshal)
    assert isinstance(_marshal, marshalled_api._GetTransacciones)
    args = [
        "0000000000000",
        1,
        "0000000000000",
        "0000000000000",
        "0000000000000",
        0,
        "2024-12-31",
        "2024-12-31",
        "2024-12-31 23:59Z-03",
        "2024-12-31 23:59Z-03",
        "2024-12-31",
        "2024-12-31",
        "R002300000000",
        "R002300000001",
        1,
        1,
        100,
        True,
    ]
    r = _marshal(*args, mock_dataset=True)
    # r = _marshal(agente_informador="0000000000000", mock_dataset=True)
    pass


def test_get_transacciones_args_null():
    operation = "GET_TRANSACCIONES"
    _marshal = marshalled_api.MARSHALS[operation]
    assert isinstance(_marshal, marshalled_api.Marshal)
    assert isinstance(_marshal, marshalled_api._GetTransacciones)
    args = [
        "0000000000000",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        "null",
        1,
        100,
        True,
    ]
    r = _marshal(*args, mock_dataset=True)
    # r = _marshal(agente_informador="0000000000000", mock_dataset=True)
    pass
