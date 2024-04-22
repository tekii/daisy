""" Marshal / UnMarshal BQ User Define Function return values and args - https://docs.python.org/3/library/marshal.html#id2 """

from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict
from datetime import datetime
from .trazamed import API

__all__ = ["Marshal", "MarshalError", "get_marshal"]


class MarshalError(ValueError):
    pass


class Marshal(metaclass=ABCMeta):
    """Manages the marshl/unmarshal to/from bq signature"""

    def __init__(self, the_api: API, method: Callable) -> None:
        self._the_api = the_api
        self._method = method

    # def __init_subclass__(cls) -> None:
    #    pass

    @abstractmethod
    def load(self, *args):
        """load the positional args of the UDF into the kw ones in the API, need to be override for each operation"""
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
        return {}

    @abstractmethod
    def dump(self, *args):
        """Ensures JSON data respond to https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type"""
        return []

    def __call__(self, *args: Any, agent_credentials: dict, mock_data: bool) -> Any:
        # this function uses only the loaded, pre conditioned dict
        # https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
        try:
            operation_specific_args = self.load(*args)
        except ValueError as e:
            raise MarshalError from e

        results = self._method(
            self._the_api,
            usuario_agente_informador=agent_credentials["user"],
            password_agente_informador=agent_credentials["password"],
            mock_data=mock_data,
            **operation_specific_args,
        )
        return self.dump(results)


class _GetTransacciones(Marshal):

    def __init__(self, the_api: API, method: Callable):
        super().__init__(the_api, method)

    def load(self, *args):
        return {
            # "agente_informador": args[0],
            "transaccion_global": None if args[1] is None else int(args[1]),
            "agente_origen": args[2],
            "agente_destino": args[3],
            "medicamento": args[4],
            "evento": None if args[5] is None else int(args[5]),
            "operacion_desde": None if args[6] is None else datetime.fromisoformat(args[6]).date(),
            "operacion_hasta": None if args[7] is None else datetime.fromisoformat(args[7]).date(),
            "transaccion_desde": None if args[8] is None else datetime.fromisoformat(args[8]),
            "transaccion_hasta": None if args[9] is None else datetime.fromisoformat(args[9]),
            "vencimiento_desde": None if args[10] is None else datetime.fromisoformat(args[10]).date(),
            "vencimiento_hasta": None if args[11] is None else datetime.fromisoformat(args[11]).date(),
            "remito": args[12],
            "factura": args[13],
            "estado": None if args[14] is None else int(args[14]),
            "pagina": None if args[15] is None else int(args[15]),
            "pagina_max_len": None if args[15] is None else int(args[15]),
        }

    def dump(self, r):
        return r


class _GetTransaccionesNoConfirmadas(Marshal):

    def __init__(self, the_api: API, method: Callable):
        super().__init__(the_api, method)

    def load(self, *args) -> dict:
        return {}

    def dump(self):
        return []


# module scope api
_api = API()

_MARSHALS: Dict[str, Marshal] = {
    "GET_TRANSACCIONES": _GetTransacciones(_api, API.get_transacciones),
    "GET_TRANSACCIONES_NO_CONFIRMADAS": _GetTransaccionesNoConfirmadas(_api, API.get_transacciones_no_confirmadas),
}


def get_marshal(operation: str) -> Marshal | None:
    # TODO: consider to raise an exception? mmm...
    return _MARSHALS.get(operation)
