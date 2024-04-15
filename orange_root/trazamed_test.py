""" test test """

import json
import pathlib
from datetime import datetime
from zeep import Client, Settings
from zeep.wsse.username import UsernameToken

# from zeep.plugins import Plugin, HistoryPlugin
import pytest


@pytest.fixture(name="target_service")
def service():

    wsdl_uri = (
        pathlib.Path(__file__).resolve().parent.joinpath("trazamed", "trazamed.wsdl").as_uri()
    )
    settings = Settings(strict=False, xml_huge_tree=False, force_https=True, raw_response=False)
    wsse = UsernameToken("testwservice", "testwservicepsw")
    client = Client(wsdl=wsdl_uri, settings=settings, wsse=wsse, plugins=[])
    _service = client.create_service(
        binding_name="{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding",
        address="https://servicios.pami.org.ar/trazamed.WebService",
    )
    return _service


# @pytest.fixture
# def client():
#    from importlib.util import spec_from_file_location, module_from_spec
#    import pathlib
#    # from importlib.machinery import SourceFileLoader
#    source = pathlib.Path(__file__).resolve().parent / "__init__.py"
#    # spec = spec_from_loader("main", SourceFileLoader("main", str(source)))
#    spec = spec_from_file_location("__test__", str(source))
#    main = module_from_spec(spec)
#    spec.loader.exec_module(main)
#    # main = SourceFileLoader("main", str(source)).load_module()
#    return main.app.test_client()


def test_01(target_service):

    response = target_service.getTransaccionesNoConfirmadas(
        "pruebasws",
        "Clave1234",
        None,
        None,
        None,
        "glnws",
        None,
        None,
        "01/01/2024",
        "01/02/2024",
        arg19=1,
        arg20=10,
    )
    assert not response.hay_error
    assert len(response.list) == 10
    # transaccionPlainWS | WEBSERVICEERROR
    _t = response.list[0]
    assert str(type(_t)) == "<class 'zeep.objects.transaccionPlainWS'>"
    id_transaccion = int(_t._id_transaccion)
    assert id_transaccion == 33071479
    # id_transaccion_global = int(_t._id_transaccion_global)
    assert _t._d_programa is None
    _ = _t._f_evento
    _f_evento = datetime.strptime(_, "%d/%m/%Y").date()
    _ = _t._f_transaccion
    _f_transaccion = datetime.strptime(_, "%d/%m/%Y %H:%M")
    # pass
    #
    # response = service.getTransaccionesNoConfirmadas(
    #    'pruebasws',
    #    'Clave1234',None,None,None,
    #    'glnws',None,None,
    #    '01/01/2024',
    #    '01/02/2024',
    #    arg19=2,
    #    arg20=10
    # )
    # assert not response.hay_error
    # assert response.list.len() == 10
    #    if not response.hay_error:
    #        for e in response.list:
    #            print(e._id_transaccion)


def test_02(target_service):
    #
    response = target_service.getConsultaStock(
        "pruebasws", "Clave1234", "00005963035960", "glnws", arg9=1, arg10=10
    )
    assert len(response.errores) == 0
    assert len(response.list) == 10
    assert response.resultado is None
    # consultaStockMedicamentoWS
    _t = response.list[0]
    assert str(type(_t)) == "<class 'zeep.objects.consultaStockMedicamentoWS'>"


def test_03(target_service):
    #
    response = target_service.getCatalogoElectronicoByGLN(
        "pruebasws", "Clave1234", arg2="glnws", arg7=1, arg8=10
    )
    # catalogoGLNResult
    assert str(type(response)) == "<class 'zeep.objects.catalogoGLNResult'>"
    assert response.hay_error is None
    assert response.cantPaginas is None
    assert response._id_generado is None
    assert response._is_modificado is None
    assert len(response.errores) == 0
    assert len(response.list) == 1
    # consultaStockMedicamentoWS
    _t = response.list[0]
    assert str(type(_t)) == "<class 'zeep.objects.agentePlain'>"


def test_04(target_service):
    #
    response = target_service.getCatalogoElectronicoByGLN(
        "pruebaswss", "Clave1234", arg2="glnws", arg7=1, arg8=10
    )
    # catalogoGLNResult
    assert str(type(response)) == "<class 'zeep.objects.catalogoGLNResult'>"
    assert response.hay_error is True
    assert response.cantPaginas is None
    assert response._id_generado is None
    assert response._is_modificado is None
    assert len(response.errores) == 1
    assert len(response.list) == 0
    # consultaStockMedicamentoWS
    _t = response.errores[0]
    assert str(type(_t)) == "<class 'zeep.objects.webServiceError'>"
    assert _t._c_error == "99999999999"
    assert _t._d_error == "Acceso denegado."


def test_05(target_service):
    #
    response = target_service.getCatalogoElectronicoByGLN(
        "pruebasws", "Clave1234444", arg2="9999999999918", arg7=1, arg8=10
    )
    # catalogoGLNResult
    assert str(type(response)) == "<class 'zeep.objects.catalogoGLNResult'>"
    assert response.hay_error is True
    assert response.cantPaginas is None
    assert response._id_generado is None
    assert response._is_modificado is None
    assert len(response.errores) == 1
    assert len(response.list) == 0
    # consultaStockMedicamentoWS
    _t = response.errores[0]
    assert str(type(_t)) == "<class 'zeep.objects.webServiceError'>"
    assert _t._c_error is None
    assert _t._d_error == " - Por favor verifique los datos ingresados. "


def test_06(target_service):
    #
    response = target_service.getTransaccionesWS(
        "pruebasws",
        "Clave1234",
        arg9="01/01/2023 02:46",
        arg10="31/12/2023",
        # arg13="R000120191004",
        arg16=4,  # ,        arg17=10, parece que retorna de a 100
    )

    # transaccionesWSResult
    assert str(type(response)) == "<class 'zeep.objects.transaccionesWSResult'>"
    assert response.hay_error is None
    assert len(response.list) > 0
    _t = response.list[0]
    assert str(type(_t)) == "<class 'zeep.objects.transaccionPlainWS'>"

    pass
