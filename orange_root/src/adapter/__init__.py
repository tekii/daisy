"""OperationAdapter / UnMarshal BQ User Define Function return values and args
- https://docs.python.org/3/library/marshal.html#id2"""

import logging
import os
import pathlib
import sys
import urllib.parse
from abc import ABCMeta, abstractmethod

# from datetime import datetime
from typing import Any, Callable, ClassVar, Dict, List, Self, Tuple  # noqa: F401

#
from zeep import Client, Settings, helpers  # noqa: F401
from zeep.proxy import OperationProxy, ServiceProxy  # noqa: F401
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken

__all__ = ["OperationAdapter", "AdapterError", "TheService"]


class AdapterError(ValueError):
    def __init__(self, *args: object, code: int) -> None:
        super().__init__(*args)
        self.code = code


class OperationAdapter(metaclass=ABCMeta):
    """Manages the marshl/unmarshal to/from bq signature"""

    _adapters: ClassVar[Dict[str, type[Self]]] = {}

    def __init__(self, op_proxy):
        self._proxy = op_proxy
        # self._proxy = op_proxy if op_proxy is not None else self._mock_data

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        name, _ = cls._name_mapping()
        OperationAdapter._adapters[name] = cls

    @classmethod
    @abstractmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("NotImplemented", "")

    @classmethod
    # @abstractmethod
    def _mock_data(self, arg0, arg1, **kwargs):
        return None

    @abstractmethod
    def load(self, *args):
        """load the positional args of the UDF into the kw ones in the API,
        need to be override for each operation"""
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
        # https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type
        return {}

    @abstractmethod
    def dump(self, results) -> List[Dict[str, Any]] | None:
        """Ensures JSON data respond to
        https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type"""
        return []

    def __call__(self, *args: Any, agent_credentials: dict) -> Any:
        # https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
        return self.dump(
            self._proxy(
                arg0=agent_credentials["user"],
                arg1=agent_credentials["password"],
                **self.load(*args)
            )
        )


class TheService(object):

    def __new__(cls):
        if not hasattr(cls, "_the_one"):
            cls._the_one = super().__new__(cls)
            cls._is_already_configured: bool = False
            cls._service_proxy: ServiceProxy
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
            # we will not attempt any handling other than pass the proper error
            # and relay on the BQ retry criteria
            transport = Transport(operation_timeout=operation_timeout)
            # not sure if i need to retain the client or the service holds the reference
            client = Client(
                wsdl=pathlib.Path(__file__).resolve().parent.joinpath("trazamed.wsdl").as_uri(),
                wsse=UsernameToken("testwservice", "testwservicepsw"),
                # transport=transport,
                settings=Settings(
                    strict=False, xml_huge_tree=False, force_https=True, raw_response=False
                ),
            )
            # instanciate the service pointing to the actual prod/test environment
            cls._service_proxy = client.create_service(
                binding_name="{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding",
                address=target_url,
            )

            cls._is_already_configured = True

        return cls._the_one

    # avoiding the temptation of make this an [] operator... 4 now or a context
    # TODO: it also can raise MethodNotFound exception or similar
    @classmethod
    def get_adapter(cls, op_ad_name: str, mock_data: bool) -> OperationAdapter:

        op_adapter_t = OperationAdapter._adapters.get(op_ad_name)
        if op_adapter_t is None:
            raise AdapterError([], code=418) from None

        if mock_data:
            op_proxy = op_adapter_t._mock_data
        else:
            _, op_real_name = op_adapter_t._name_mapping()
            op_proxy = cls._service_proxy[op_real_name]

        return op_adapter_t(op_proxy)
