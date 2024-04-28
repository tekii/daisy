import pathlib
import pytest
import json
from datetime import date, datetime

from . import Api, TransaccionesResponse


@pytest.fixture(name="the_entrenamiento_api")
def devel_api():
    api = Api(address="https://servicios.pami.org.ar/trazamed.WebService", operation_timeout=600)
    return api


@pytest.fixture(name="the_production_api")
def prod_api():
    api = Api(address="https://trazabilidad.pami.org.ar:9050/trazamed.WebService", operation_timeout=600)
    return api


@pytest.fixture(name="the_production_secrets")
def prod_secrets():
    fn = pathlib.Path(__file__).resolve().parent.joinpath("secrets.json")
    with open(fn) as f:
        secrets = json.load(f)
        return secrets


def test_TransaccionesResponse_mock(the_entrenamiento_api):
    assert len(TransaccionesResponse._mock_data) == 460
    pass


@pytest.mark.skip
def test_get_transacciones_103_results(the_entrenamiento_api):

    result = the_entrenamiento_api.get_transacciones(
        "pruebasws",
        "Clave1234",
        f_transaccion_desde=datetime.fromisoformat("2023-02-01T02:46"),
        f_transaccion_hasta=datetime.fromisoformat("2023-02-28"),
        pagina=1,
        pagina_max_len=50,
    )
    assert len(result) == 100

    result = the_entrenamiento_api.get_transacciones(
        "pruebasws",
        "Clave1234",
        f_transaccion_desde=datetime.fromisoformat("2023-02-01T02:46"),
        f_transaccion_hasta=datetime.fromisoformat("2023-02-28"),
        pagina=2,
        pagina_max_len=50,
    )
    assert len(result) == 3


@pytest.mark.skip
def test_get_transacciones_from_prod(the_production_api, the_production_secrets):

    user = the_production_secrets["user"]
    password = the_production_secrets["password"]
    result = the_production_api.get_transacciones(
        user,
        password,
        f_transaccion_desde=datetime.fromisoformat("2013-08-01"),
        f_transaccion_hasta=datetime.fromisoformat("2013-09-30"),
        pagina=2,
        pagina_max_len=50,
    )
    assert len(result) == 100
