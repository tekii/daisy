""" Marshal / UnMarshal BQ User Define Function return values and args - https://docs.python.org/3/library/marshal.html#id2 """

from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict
from trazamed import API

__all__ = ["Marshal", "MARSHALS"]


class Marshal(metaclass=ABCMeta):
    """Manages the marshl/unmarshal to/from bq signature"""

    def __init__(self, the_api: API, method: Callable) -> None:
        self._the_api = the_api
        self._method = method

    # def __init_subclass__(cls) -> None:
    #    pass

    @abstractmethod
    def load(self, *args: Any, **kwds: Any):
        pass

    @abstractmethod
    def dump(self):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        _args, _kwds = self.load(*args, **kwds)
        raw = self._method(self._the_api, *_args, **_kwds)
        return self.dump()


class _GetTransacciones(Marshal):

    def __init__(self, the_api: API, method: Callable):
        super().__init__(the_api, method)

    def load(self, *args: Any, **kwds: Any):
        _0 = args[0]
        _1 = args[1]
        # IndexError
        return args[0], kwds

    def dump(self):
        pass


class _GetTransaccionesNoConfirmadas(Marshal):

    def __init__(self, the_api: API, method: Callable):
        super().__init__(the_api, method)

    def load(self, *args: Any, **kwds: Any):
        pass

    def dump(self):
        pass


# module scope api
_api = API()

MARSHALS: Dict[str, Marshal] = {
    "GET_TRANSACCIONES": _GetTransacciones(_api, API.get_transacciones),
    "GET_TRANSACCIONES_NO_CONFIRMADAS": _GetTransaccionesNoConfirmadas(_api, API.get_transacciones_no_confirmadas),
}
