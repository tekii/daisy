from datetime import datetime
from typing import Any, List, Dict, Tuple
from zeep import helpers
from zeep.proxy import OperationProxy
from . import OperationAdapter, AdapterError

__all__ = [
    "_GetTransaccionesNoConfirmadasAdapter",
]


class _GetTransaccionesNoConfirmadasAdapter(OperationAdapter):

    @classmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("GET_TRANSACCIONES_NO_CONFIRMADAS", "getTransaccionesNoConfirmadas")

    def load(self, *args) -> dict:
        try:
            return {
                # "arg0"=usuario_agente_informador,
                # "arg1"=password_agente_informador,
                "arg2": None if args[1] is None else int(args[1]),  # transaccion_global
                "arg3": args[0],  # gln_agente_informador
                "arg4": args[3],  # gln_agente_origen
                "arg5": args[4],  # gln_agente_destino
                "arg6": args[5],  # gtin_medicamento
                "arg7": None if args[6] is None else int(args[6]),  # id_evento,
                "arg8": None if args[7] is None else datetime.fromisoformat(args[7]).strftime("%d/%m/%Y"),  # f_transaccion_desde
                "arg9": None if args[8] is None else datetime.fromisoformat(args[8]).strftime("%d/%m/%Y"),  # f_transaccion_hasta
                "arg10": None if args[9] is None else datetime.fromisoformat(args[9]).date().strftime("%d/%m/%Y"),  # f_operacion_desde
                "arg11": None if args[10] is None else datetime.fromisoformat(args[10]).date().strftime("%d/%m/%Y"),  # f_operacion_hasta
                "arg12": None if args[11] is None else datetime.fromisoformat(args[11]).date().strftime("%d/%m/%Y"),  # f_vencimiento_desde
                "arg13": None if args[12] is None else datetime.fromisoformat(args[12]).date().strftime("%d/%m/%Y"),  # f_vencimiento_hasta
                "arg14": args[13],  # remito
                "arg15": args[14],  # factura
                "arg16": None if args[15] is None else int(args[15]),  #  id_estado
                "arg17": args[16],  # lote
                "arg18": args[17],  # serie
                "arg19": None if args[18] is None else int(args[18]),  #  pagina
                "arg20": None if args[19] is None else int(args[19]),  #  pagina_max_result
            }
        except ValueError as e:
            raise AdapterError(*e.args, code=400) from None

    def dump(self, results):
        return results
