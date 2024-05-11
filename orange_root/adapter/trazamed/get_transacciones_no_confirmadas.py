from typing import Any, Dict, List
from datetime import date, datetime

#from . import Api


def get_transacciones_no_confirmadas(
    self,
    #
    usuario_agente_informador: str,  # arg0
    password_agente_informador: str,  # arg1
    transaccion_global: int | None = None,  # arg2
    gln_agente_informador: str | None = None,  # arg3
    gln_agente_origen: str | None = None,  # arg4
    gln_agente_destino: str | None = None,  # arg5
    gtin_medicamento: str | None = None,  # arg6
    id_evento: int | None = None,  # arg7
    f_transaccion_desde: date | None = None,  # arg8
    f_transaccion_hasta: date | None = None,  # arg9
    f_operacion_desde: date | None = None,  # arg10
    f_operacion_hasta: date | None = None,  # arg11
    f_vencimiento_desde: date | None = None,  # arg12
    f_vencimiento_hasta: date | None = None,  # arg13
    remito: str | None = None,  # arg14
    factura: str | None = None,  # arg15
    id_estado: int | None = None,  # arg16
    lote: str | None = None,  # arg17
    serie: str | None = None,  # arg18
    pagina: int | None = None,  # arg19
    pagina_max_result: int | None = None,  # arg20
    mock_data: bool = False,
    #
) -> List[Dict[str, Any]] | None:

    if mock_data:

        return None
    
    else:

        response = self._service.getTransaccionesNoConfirmadas(
            arg0=usuario_agente_informador,
            arg1=password_agente_informador,
            arg2=transaccion_global,
            arg3=gln_agente_informador,
            arg4=gln_agente_origen,
            arg5=gln_agente_destino,
            arg6=gtin_medicamento,
            arg7=id_evento,
            arg8=None if f_transaccion_desde is None else f_transaccion_desde.strftime("%d/%m/%Y"),
            arg9=None if f_transaccion_hasta is None else f_transaccion_hasta.strftime("%d/%m/%Y"),
            arg10=None if f_operacion_desde is None else f_operacion_desde.strftime("%d/%m/%Y"),
            arg11=None if f_operacion_hasta is None else f_operacion_hasta.strftime("%d/%m/%Y"),
            arg12=None if f_vencimiento_desde is None else f_vencimiento_desde.strftime("%d/%m/%Y"),
            arg13=None if f_vencimiento_hasta is None else f_vencimiento_hasta.strftime("%d/%m/%Y"),
            arg14=remito,
            arg15=factura,
            arg16=id_estado,
            arg17=lote,
            arg18=serie,
            arg19=pagina,
            arg20=pagina_max_result,
        )
        return None if response is None else response.list
