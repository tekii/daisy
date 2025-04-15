import pytest
from datetime import date, datetime

from . import Api


@pytest.fixture(name="the_entrenamiento_api")
def devel_api():
    api = Api(address="https://servicios.pami.org.ar/trazamed.WebService", operation_timeout=600)
    return api


def test_get_transacciones_no_confirmadas(the_entrenamiento_api):

    result = the_entrenamiento_api.get_transacciones_no_confirmadas(
        "pruebasws",
        "Clave1234",
        #f_transaccion_desde=date.fromisoformat("2023-02-01"),
        #f_transaccion_hasta=date.fromisoformat("2023-02-28"),
        pagina=284,
        pagina_max_result=1000,
    )
    assert len(result) == 100