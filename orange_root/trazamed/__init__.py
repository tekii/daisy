""" Trazmed """

# mypy: disable-error-code="valid-type"

from datetime import date, datetime
from typing import List
import pathlib

from zeep import Client, Settings
from zeep.wsse.username import UsernameToken
from zeep.plugins import Plugin, HistoryPlugin
from zeep.transports import Transport

__version__ = "0.0.1"
__all__ = [
    "API",
]

# mypy: disable-error-code="valid-type"
type GLN = str
type GTIN = str
type FC = str


class TrazamedService:

    def __init__(self):

        wsdl_uri = pathlib.Path(__file__).resolve().parent.joinpath("trazamed", "trazamed.wsdl").as_uri()
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


class TransaccionesNoConfirmadasResponse:
    pass


class TransaccionesResponse:
    pass


class API:
    """Python friendly wrapper arround the not so beautiful Trazamed SOAP API"""

    def __init__(self) -> None:
        pass

    def get_transacciones_no_confirmadas(
        self,
        agente_informador: GLN,
        # usuario_agente: str,  # change this to interna dict
        # usuario_password: str,
        transaccion_global: int | None = None,  # arg2
        agente_origen: GLN | None = None,  # arg3
        agente_destino: GLN | None = None,  # arg4
        medicamento: GTIN | None = None,  # arg5
        evento: int | None = None,  # arg6
        operacion_desde: date | None = None,  # arg7
        operacion_hasta: date | None = None,  # arg8
        transaccion_desde: datetime | None = None,  # arg9
        transaccion_hasta: datetime | None = None,  # arg10
        vencimiento_desde: date | None = None,  # arg11
        vencimiento_hasta: date | None = None,  # arg12
        remito: FC | None = None,  # arg13
        factura: FC | None = None,  # arg14
        estado: int | None = None,  # arg15
        lote: str | None = None,  # arg16
        serie: str | None = None,  # arg??
        arg18: str | None = None,  # arg18
        pagina: int | None = None,  # arg19
        paginaMaxLen: int | None = None,  # arg20
        mock_dataset: bool = False,
    ) -> TransaccionesNoConfirmadasResponse | None:
        return None

    def get_transacciones(
        self,
        agente_informador: GLN,
        # usuario_agente: str,  # change this to interna dict
        # usuario_password: str,
        transaccion_global: int | None = None,  # arg2
        agente_origen: GLN | None = None,  # arg3
        agente_destino: GLN | None = None,  # arg4
        medicamento: GTIN | None = None,  # arg5
        evento: int | None = None,  # arg6
        operacion_desde: date | None = None,  # arg7
        operacion_hasta: date | None = None,  # arg8
        transaccion_desde: datetime | None = None,  # arg9
        transaccion_hasta: datetime | None = None,  # arg10
        vencimiento_desde: date | None = None,  # arg11
        vencimiento_hasta: date | None = None,  # arg12
        remito: FC | None = None,  # arg13
        factura: FC | None = None,  # arg14
        estado: int | None = None,  # arg15
        pagina: int | None = None,  # arg16
        paginaMaxLen: int | None = None,  # arg17
        mock_dataset: bool = False,
    ) -> TransaccionesResponse | None:
        return None
