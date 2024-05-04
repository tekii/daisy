""" Marshal / UnMarshal BQ User Define Function return values and args - https://docs.python.org/3/library/marshal.html#id2 """

import os
import sys
import urllib.parse
import logging
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, List
from datetime import datetime
from zeep import helpers
from .trazamed import Api

__all__ = ["Marshal", "MarshalError", "get_marshal"]


class MarshalError(ValueError):
    def __init__(self, *args: object, code: int) -> None:
        super().__init__(*args)
        self.code = code


class Marshal(metaclass=ABCMeta):
    """Manages the marshl/unmarshal to/from bq signature"""

    def __init__(self, the_api: Api, method: Callable) -> None:
        self._the_api = the_api
        self._method = method

    # def __init_subclass__(cls) -> None:
    #    pass

    @abstractmethod
    def load(self, *args):
        """load the positional args of the UDF into the kw ones in the API, need to be override for each operation"""
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
        # https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type
        return {}

    @abstractmethod
    def dump(self, results) -> List[Dict[str, Any]] | None:
        """Ensures JSON data respond to https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type"""
        return []

    def __call__(self, *args: Any, agent_credentials: dict, mock_data: bool) -> Any:
        # this function uses only the loaded, pre conditioned dict args
        # https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
        return self.dump(
            self._method(
                self._the_api,
                usuario_agente_informador=agent_credentials["user"],
                password_agente_informador=agent_credentials["password"],
                mock_data=mock_data,
                **self.load(*args)
            )
        )


class _GetTransacciones(Marshal):

    def __init__(self, the_api: Api, method: Callable):
        super().__init__(the_api, method)

    def load(self, *args):
        try:
            return {
                # [indexes] here comes from the BigQuery params order and arg0 is the agent
                "transaccion_global": None if args[1] is None else int(args[1]),
                "gln_agente_origen": args[2],
                "gln_agente_destino": args[3],
                "gtin_medicamento": args[4],
                "id_evento": None if args[5] is None else int(args[5]),
                "f_operacion_desde": None if args[6] is None else datetime.fromisoformat(args[6]).date(),
                "f_operacion_hasta": None if args[7] is None else datetime.fromisoformat(args[7]).date(),
                "f_transaccion_desde": None if args[8] is None else datetime.fromisoformat(args[8]),
                "f_transaccion_hasta": None if args[9] is None else datetime.fromisoformat(args[9]),
                "f_vencimiento_desde": None if args[10] is None else datetime.fromisoformat(args[10]).date(),
                "f_vencimiento_hasta": None if args[11] is None else datetime.fromisoformat(args[11]).date(),
                "remito": args[12],
                "factura": args[13],
                "estado": None if args[14] is None else int(args[14]),
                "pagina": None if args[15] is None else int(args[15]),
            }
        except ValueError as e:
            raise MarshalError(*e.args, code=400) from None

    def dump(self, results) -> List[Dict[str, Any]] | None:
        if results is None:
            return None
        else:
            try:
                dumped = []
                for r in results:
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
                raise MarshalError(*e.args, code=418) from None


class _GetTransaccionesNoConfirmadas(Marshal):

    def __init__(self, the_api: Api, method: Callable):
        super().__init__(the_api, method)

    def load(self, *args) -> dict:
        return {}

    def dump(self):
        return []


_target_url = os.environ.get("TARGET_URL")
if _target_url is None:
    logging.fatal("TARGET_URL undefined.")
    sys.exit(1)
else:
    try:
        _target_url = urllib.parse.unquote(_target_url)
    except TypeError as e:
        pass

_connect_timeout = os.environ.get("CONNECT_TIMEOUT")
_read_timeout = os.environ.get("READ_TIMEOUT")
if not _connect_timeout or not _read_timeout:
    logging.fatal("CONNECT_TIMEOUT or READ_TIMEOUT undefined.")
    sys.exit(1)

try:
    _timeout = (float(_connect_timeout), float(_read_timeout))
except ValueError as e:
    logging.fatal("CONNECT_TIMEOUT or READ_TIMEOUT NaN.")
    sys.exit(1)

# module scope api
_api = Api(address=_target_url, operation_timeout=_timeout)

_MARSHALS: Dict[str, Marshal] = {
    "GET_TRANSACCIONES": _GetTransacciones(_api, Api.get_transacciones),
    "GET_TRANSACCIONES_NO_CONFIRMADAS": _GetTransaccionesNoConfirmadas(_api, Api.get_transacciones_no_confirmadas),
}


def get_marshal(operation: str) -> Marshal | None:
    # TODO: consider to raise an exception? mmm...
    return _MARSHALS.get(operation)
