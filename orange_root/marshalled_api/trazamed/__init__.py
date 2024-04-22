""" Trazmed """

from typing import Any, Dict, List
from datetime import date, datetime
import pathlib
from zeep import Client, Settings
from zeep.wsse.username import UsernameToken
from zeep.plugins import Plugin, HistoryPlugin
from zeep.transports import Transport
from zeep import helpers

__version__ = "0.0.0"
__all__ = [
    "Api",
]

type GLN = str  # valid-type: ignore
type GTIN = str  # mypy: disable-error-code="valid-type"
type FC = str


class TransaccionesNoConfirmadasResponse:
    pass


class TransaccionesResponse:

    _mock_data = []
    _MOCK = {
        "_d_evento": "ENVIO DE PRODUCTO EN CARACTER DEVOLUCION POR PROHIBICION",
        "_d_programa": None,
        "_f_evento": "12/01/2024",
        "_f_transaccion": "11/01/2024 16:17",
        "_gln_destino": "glnws",
        "_gln_origen": "9992209100005",
        "_gtin": "00005963035960",
        "_id_detalle_evento": None,
        "_id_estado": None,
        "_id_evento": 20,
        "_id_transaccion": 33071479,
        "_id_transaccion_global": 37540651,
        "_lote": "16",
        "_n_factura": "a111112233444",
        "_n_remito": "a1121121111112",
        "_nombre": " CAPECITABINA FILAXIS ",
        "_numero_serial": "20",
        "_razon_social_destino": "LABORATORIO",
        "_razon_social_origen": "farmacia",
        "_vencimiento": "07/01/2015",
        "_ver2_paciente_apellido": None,
        "_ver2_paciente_documento": None,
        "_ver2_paciente_id_documento": None,
        "_ver2_paciente_id_obra_social": None,
        "_ver2_paciente_nombre": None,
        "_ver2_paciente_numero_afiliado": None,
    }

    _loop = 0
    while True:
        _new_one = _MOCK.copy()
        _new_one["_id_transaccion"] += _loop  # type: ignore
        _mock_data.append(_new_one)
        _loop += 1
        if 460 == _loop:
            break

    def __init__(self) -> None:
        pass

    @staticmethod
    def return_mock_data(page_num, page_len) -> List[Dict[str, Any]] | None:
        offset = (page_num - 1) * page_len
        page_data = TransaccionesResponse._mock_data[offset : offset + page_len]
        return None if len(page_data) == 0 else page_data


class Api:
    """Python friendly wrapper arround the not so beautiful Trazamed SOAP API"""

    def __init__(self, address="https://servicios.pami.org.ar/trazamed.WebService"):

        # uses the local wsdl file placed in the same folder of this file
        wsdl = pathlib.Path(__file__).resolve().parent.joinpath("trazamed.wsdl").as_uri()
        #
        settings = Settings(strict=False, xml_huge_tree=False, force_https=True, raw_response=False)
        # yes its sad...
        wsse = UsernameToken("testwservice", "testwservicepsw")
        # not sure if i need to retain the client or the service holds the reference
        self._client = Client(wsdl=wsdl, settings=settings, wsse=wsse)
        # instanciate the service pointing to the actual prod/test environment
        self._service = self._client.create_service(
            binding_name="{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding",
            address=address,
        )

    def get_transacciones_no_confirmadas(
        self,
        # usuario_agente_informador: str,  # change this to interna dict
        # usuario_password_informador: str,
        agente_informador: GLN,
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
        mock_data: bool = False,
    ) -> List[Dict[str, Any]] | None:
        return None

    def get_transacciones(
        self,
        #
        usuario_agente_informador: str,  # arg0
        password_agente_informador: str,  # arg1
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
        pagina_max_len: int | None = None,  # arg17
        #
        mock_data: bool = False,
        #
    ) -> List[Dict[str, Any]] | None:
        """return transacciones"""

        if mock_data:
            return TransaccionesResponse.return_mock_data(pagina, pagina_max_len)
        else:
            response = self._service.getTransaccionesWS(
                arg0=usuario_agente_informador,
                arg1=password_agente_informador,
                arg2=transaccion_global,
                arg3=agente_origen,
                arg4=agente_destino,
                arg5=medicamento,
                arg6=evento,
                arg7=None if operacion_desde is None else operacion_desde.strftime("%d/%m/&%Y"),
                arg8=None if operacion_hasta is None else operacion_hasta.strftime("%d/%m/%Y"),
                arg9=None if transaccion_desde is None else transaccion_desde.strftime("%d/%m/%Y %H:%M"),
                arg10=None if transaccion_hasta is None else transaccion_hasta.strftime("%d/%m/%Y %H:%M"),
                arg11=None if vencimiento_desde is None else vencimiento_desde.strftime("%d/%m/&%Y"),
                arg12=None if vencimiento_hasta is None else vencimiento_hasta.strftime("%d/%m/%Y"),
                arg13=remito,
                arg14=factura,
                arg15=estado,
                arg16=pagina,
                # arg17=pagina_max_len,
            )

            return helpers.serialize_object(response.list, dict)
