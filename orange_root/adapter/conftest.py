import pytest
from . import *

@pytest.fixture(autouse=False)
def testing_service(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https%3A%2F%2Fservicios.pami.org.ar%2Ftrazamed.WebService")
    monkeypatch.setenv("CONNECT_TIMEOUT", "30")
    monkeypatch.setenv("READ_TIMEOUT", "1800")
    # seems to be that isinstance doesnt works because the multiple import paths...
    #mod = importlib.import_module("marshals","..marshals")
#    from .marshals import TheMarshallers 
    #from .marshals import TheMarshallers
    service = TheService().configure_or_die()
    yield service
    #tm = TheService()
    #tm._is_already_configured = False
    #tm._marshals = {}

@pytest.fixture()
def entrenamiento_credentials():
    return {"user": "pruebasws", "password": "Clave1234"}