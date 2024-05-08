""" OperationAdapter / UnMarshal BQ User Define Function return values and args - https://docs.python.org/3/library/marshal.html#id2 """

import os
import pathlib
import sys
import urllib.parse
import logging
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, ClassVar, Dict, List, Self, Tuple
from datetime import datetime
from zeep import Client, Settings, helpers
from zeep.transports import Transport
from zeep.proxy import ServiceProxy, OperationProxy
from zeep.wsse.username import UsernameToken
from .trazamed import Api

__all__ = ["OperationAdapter", "MarshalError", "TheService"]


class MarshalError(ValueError):
    def __init__(self, *args: object, code: int) -> None:
        super().__init__(*args)
        self.code = code


class OperationAdapter(metaclass=ABCMeta):
    """Manages the marshl/unmarshal to/from bq signature"""

    _adapters: ClassVar[Dict[str, type[Self]]] = {}

    def __init__(self, op_proxy: OperationProxy) -> None:
        # self._the_api = the_api
        self._proxy: OperationProxy = op_proxy  # type: ignore
        # self._method = method

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        name, _ = cls._name_mapping()
        OperationAdapter._adapters[name] = cls

    @classmethod
    @abstractmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("NotImplemented", "")

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
        #       mock_data=mock_data,
        return self.dump(

           self._proxy(
               arg0=agent_credentials["user"],
               arg1=agent_credentials["password"],
               **self.load(*args)
           )

        )


class _GetTransaccionesAdapter(OperationAdapter):

    def __init__(self, op_proxy: OperationProxy):
        super().__init__(op_proxy=op_proxy)

    @classmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("GET_TRANSACCIONES", "getTransaccionesWS")

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
            raise MarshalError(*e.args, code=400) from None

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
                raise MarshalError(*e.args, code=418) from None


class _GetTransaccionesNoConfirmadasAdapter(OperationAdapter):

    def __init__(self, op_proxy: OperationProxy):
        super().__init__(op_proxy=op_proxy)

    @classmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("GET_TRANSACCIONES_NO_CONFIRMADAS", "getTransaccionesNoConfirmadas")

    def load(self, *args) -> dict:
        return {}

    def dump(self):
        return []


class TheService(object):

    def __new__(cls):
        if not hasattr(cls, "_the_one"):
            cls._the_one = super().__new__(cls)
            cls._is_already_configured: bool = False
            cls._service_proxy: ServiceProxy
            cls._adapters: Dict[str, type[OperationAdapter]]  # = {}
        return cls._the_one

    @classmethod
    def configure_or_die(cls):
        #
        if not cls._is_already_configured:
            # dev or prod
            encoded_target_url = os.environ.get("TARGET_URL")
            if encoded_target_url is None:
                logging.fatal("TARGET_URL undefined.")
                sys.exit(1)
            else:
                try:
                    target_url = urllib.parse.unquote(encoded_target_url)
                except TypeError as e:
                    logging.fatal("Error unquoting TARGET_URL.")
                    sys.exit(1)
            # timeouts
            connect_timeout = os.environ.get("CONNECT_TIMEOUT")
            read_timeout = os.environ.get("READ_TIMEOUT")
            if not connect_timeout or not read_timeout:
                logging.fatal("CONNECT_TIMEOUT or READ_TIMEOUT undefined.")
                sys.exit(1)
            try:
                operation_timeout = (float(connect_timeout), float(read_timeout))
            except ValueError as e:
                logging.fatal("CONNECT_TIMEOUT or READ_TIMEOUT NaN.")
                sys.exit(1)
            # TODO check the allow max times in Cloud functions and BigQuery
            # we will not attempt any handling other than pass the proper error and relay on the BQ retry criteria
            transport = Transport(operation_timeout=operation_timeout)
            # not sure if i need to retain the client or the service holds the reference
            client = Client(
                wsdl=pathlib.Path(__file__).resolve().parent.joinpath("trazamed", "trazamed.wsdl").as_uri(),
                wsse=UsernameToken("testwservice", "testwservicepsw"),
                # transport=transport,
                settings=Settings(strict=False, xml_huge_tree=False, force_https=True, raw_response=False),
            )
            # instanciate the service pointing to the actual prod/test environment
            cls._service_proxy = client.create_service(
                binding_name="{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding",
                address=target_url,
            )

            cls._is_already_configured = True

    # avoiding the temptation of make this an [] operator... 4 now or a context
    # TODO: it also can raise MethodNotFound exception or similar
    @classmethod
    def get_adapter(cls, op_ad_name: str) -> OperationAdapter | None:

        op_adapter_t = OperationAdapter._adapters.get(op_ad_name)
        if op_adapter_t is None:
            raise MarshalError([], code=418) from None

        _, op_real_name = op_adapter_t._name_mapping()

        op_proxy = cls._service_proxy[op_real_name]

        op_adapter = op_adapter_t(op_proxy=op_proxy)

        return op_adapter
