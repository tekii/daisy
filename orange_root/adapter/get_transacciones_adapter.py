from datetime import datetime
from typing import Any, List, Dict, Tuple
from zeep import helpers
from zeep.proxy import OperationProxy
from .adapter import OperationAdapter, AdapterError

__all__ = [
    "_GetTransaccionesAdapter",
]


class _GetTransaccionesAdapter(OperationAdapter):

    def __init__(self, op_proxy: OperationProxy):
        super().__init__(op_proxy=op_proxy)

    @classmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("GET_TRANSACCIONES", "getTransaccionesWS")

    @classmethod
    def _mock_data(cls, *args):
        page_num = args[15]
        page_len = 100
        offset = (page_num - 1) * page_len
        page_data = cls._mock_data_[offset : offset + page_len]
        return None if len(page_data) == 0 else page_data

    def load(self, *args):
        try:
            return {
                # None,
                # None,
                "arg2": None if args[1] is None else int(args[1]),  # transaccion_global
                "arg3": args[2],  # gln_agente_origen
                "arg4": args[3],  # gln_agente_destino
                "arg5": args[4],  # gtin_medicamento
                "arg6": None if args[5] is None else int(args[5]),  # arg6 id_evento
                "arg7": None if args[6] is None else datetime.fromisoformat(args[6]).date().strftime("%d/%m/%Y"),  # f_operacion_desde
                "arg8": None if args[7] is None else datetime.fromisoformat(args[7]).date().strftime("%d/%m/%Y"),  # f_operacion_hasta
                "arg9": None if args[8] is None else datetime.fromisoformat(args[8]).strftime("%d/%m/%Y %H:%M"),  # f_transaccion_desde
                "arg10": None if args[9] is None else datetime.fromisoformat(args[9]).strftime("%d/%m/%Y %H:%M"),  # f_transaccion_hasta
                "arg11": None if args[10] is None else datetime.fromisoformat(args[10]).date().strftime("%d/%m/%Y"),  # f_vencimiento_desde
                "arg12": None if args[11] is None else datetime.fromisoformat(args[11]).date().strftime("%d/%m/%Y"),  # f_vencimiento_hasta
                "arg13": args[12],  # remito
                "arg14": args[13],  # factura
                "arg15": None if args[14] is None else int(args[14]),  #  estado
                "arg16": None if args[15] is None else int(args[15]),  #  pagina
            }
        except ValueError as e:
            raise AdapterError(*e.args, code=400) from None

    def dump(self, results) -> List[Dict[str, Any]] | None:
        if results is None:
            return None
        else:
            try:
                dumped = []
                for r in results.list:
                    d = helpers.serialize_object(r, dict)
                    d["_f_evento"] = (
                        None if d["_f_evento"] is None else datetime.strptime(d["_f_evento"], "%d/%m/%Y").date().strftime("%Y-%m-%d")
                    )
                    d["_f_transaccion"] = (
                        None
                        if d["_f_transaccion"] is None
                        else datetime.strptime(d["_f_transaccion"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%dT%H:%M")
                    )
                    d["_vencimiento"] = (
                        None if d["_vencimiento"] is None else datetime.strptime(d["_vencimiento"], "%d/%m/%Y").date().strftime("%Y-%m-%d")
                    )
                    d["_id_estado"] = None if d["_id_estado"] is None else int(d["_id_estado"])
                    d["_id_evento"] = None if d["_id_evento"] is None else int(d["_id_evento"])
                    d["_id_detalle_evento"] = None if d["_id_detalle_evento"] is None else int(d["_id_detalle_evento"])
                    del d["_ver2_paciente_apellido"]
                    del d["_ver2_paciente_documento"]
                    del d["_ver2_paciente_id_documento"]
                    del d["_ver2_paciente_id_obra_social"]
                    del d["_ver2_paciente_nombre"]
                    del d["_ver2_paciente_numero_afiliado"]
                    dumped.append(d)

                return dumped

            except ValueError as e:
                # this is an attemp to diferentiate of the ValueErrors in the request
                raise AdapterError(*e.args, code=418) from None

    _mock_data_ = []
    _MOCK_ROW = {
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
    for n in range(460):
        row = _MOCK_ROW.copy()
        row["_id_transaccion"] += n  # type: ignore
        _mock_data_.append(row)
