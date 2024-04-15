""" Trazmed """

from datetime import date
import string

# from typing import List

import pathlib

from zeep import Client, Settings
from zeep.wsse.username import UsernameToken
from zeep.plugins import Plugin, HistoryPlugin

__version__ = "0.0.1"
__all__ = [
    "getRelay",
]

type GLN = string
type GTIN = string
type FC = string


class TrazamedService:

    def __init__(self):

        wsdl_uri = (
            pathlib.Path(__file__).resolve().parent.joinpath("trazamed", "trazamed.wsdl").as_uri()
        )
        settings = Settings(strict=False, xml_huge_tree=False, force_https=True, raw_response=False)
        wsse = UsernameToken("testwservice", "testwservicepsw")
        client = Client(wsdl=wsdl_uri, settings=settings, wsse=wsse, plugins=[])
        self._service = client.create_service(
            binding_name="{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding",
            address="https://servicios.pami.org.ar/trazamed.WebService",
        )

    class TransaccionesResult:
        def __init__(self):
            pass

    def getTransacciones(self, credentials) -> TransaccionesResult | None:
        return None


class TransaccionesNoConfirmadasWSResult:
    pass


def getTransaccionesNoConfirmadas(
    usuarioAgente: string,
    usuarioPassword: string,
    transaccionGlobal: int = None,
    agenteInformador: GLN = None,
    agenteOrigen: GLN = None,
    agenteDestino: GLN = None,
    medicamento: GTIN = None,
    evento: int = None,
    transaccionDesde: date = None,
    transaccionHasta: date = None,
    operacionesde: date = None,
    operacionHasta: date = None,
    vencimientoDesde: date = None,
    vencimientoHasta: date = None,
    remito: FC = None,
    factura: FC = None,
    estado: int = None,
    lote: string = None,
    serie: string = None,
    pagina: int = None,
    paginaMaxLen: int = None,
) -> TransaccionesNoConfirmadasWSResult | None:
    return None


## getEnviosPropiosAlertados
## getConsultaStock
# history = HistoryPlugin()
# wsdl = pathlib.Path(__file__).resolve().parent / "trazamed.wsdl"
## wsdl='https://servicios.pami.org.ar/trazamed.WebService?wsdl'
# wsdl = wsdl.as_uri()
# settings = Settings(strict=False, xml_huge_tree=False, force_https=True, raw_response=False)
# wsse = UsernameToken("testwservice", "testwservicepsw")
# client = Client(wsdl=wsdl, settings=settings, wsse=wsse, plugins=[history])
# service = client.create_service(
#    binding_name="{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding",
#    address="https://servicios.pami.org.ar/trazamed.WebService",
# )


# def getTransaccionesNoConfirmadas_relay(agent_credentials: dict, call: list):
#
#    the_response = service.getTransaccionesNoConfirmadas(
#        "pruebasws",
#        "Clave1234",
#        None,
#        None,
#        None,
#        "glnws",
#        None,
#        None,
#        "01/01/2024",
#        "15/01/2024",
#        arg19=2,
#        arg20=2,
#    )
#
#    if not the_response.hay_error:
#        print(len(the_response.list))
#        print(the_response.cantPaginas)
#        for e in the_response.list:
#
#            print(e._id_transaccion)
#
#    return [None, 1, 2, "tree"]
#


def getRelay(operation: string):
    if operation == "getTransaccionesNoConfirmadas":
        return getTransaccionesNoConfirmadas_relay
    else:
        abort(500, description="Invalid operation: {operation}")
