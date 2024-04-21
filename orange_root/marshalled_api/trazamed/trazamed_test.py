import pytest

from . import API, TransaccionesResponse


@pytest.fixture(name="API")
def the_api():
    return API


def test_TransaccionesResponse_mock(API):
    assert len(TransaccionesResponse._mock_data) == 460
    pass
