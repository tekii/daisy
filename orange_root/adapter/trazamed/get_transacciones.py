from datetime import date, datetime


def get_transacciones(
    self,
    #
    usuario_agente_informador: str,  # arg0
    password_agente_informador: str,  # arg1
    transaccion_global: int | None = None,  # arg2
    gln_agente_origen: str | None = None,  # arg3
    gln_agente_destino: str | None = None,  # arg4
    gtin_medicamento: str | None = None,  # arg5
    id_evento: int | None = None,  # arg6
    f_operacion_desde: date | None = None,  # arg7
    f_operacion_hasta: date | None = None,  # arg8
    f_transaccion_desde: datetime | None = None,  # arg9
    f_transaccion_hasta: datetime | None = None,  # arg10
    f_vencimiento_desde: date | None = None,  # arg11
    f_vencimiento_hasta: date | None = None,  # arg12
    remito: str | None = None,  # arg13
    factura: str | None = None,  # arg14
    estado: int | None = None,  # arg15
    pagina: int | None = None,  # arg16
    pagina_max_len: int | None = None,  # arg17
    #
    mock_data: bool = False,
    #
):  # -> List[Dict[str, Any]] | None:
    """return transacciones"""
    if mock_data:
        return TransaccionesResponse.return_mock_data(pagina, 100 if pagina_max_len is None else pagina_max_len)
    else:
        response = self._service.getTransaccionesWS(
            arg0=usuario_agente_informador,
            arg1=password_agente_informador,
            arg2=transaccion_global,
            arg3=gln_agente_origen,
            arg4=gln_agente_destino,
            arg5=gtin_medicamento,
            arg6=id_evento,
            arg7=None if f_operacion_desde is None else f_operacion_desde.strftime("%d/%m/%Y"),
            arg8=None if f_operacion_hasta is None else f_operacion_hasta.strftime("%d/%m/%Y"),
            arg9=None if f_transaccion_desde is None else f_transaccion_desde.strftime("%d/%m/%Y %H:%M"),
            arg10=None if f_transaccion_hasta is None else f_transaccion_hasta.strftime("%d/%m/%Y %H:%M"),
            arg11=None if f_vencimiento_desde is None else f_vencimiento_desde.strftime("%d/%m/%Y"),
            arg12=None if f_vencimiento_hasta is None else f_vencimiento_hasta.strftime("%d/%m/%Y"),
            arg13=remito,
            arg14=factura,
            arg15=estado,
            arg16=pagina,
            # arg17=pagina_max_len,
        )
        # return helpers.serialize_object(response.list, dict)
        return None if response is None else response.list
