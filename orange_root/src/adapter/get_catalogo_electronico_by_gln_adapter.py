from datetime import datetime
from types import SimpleNamespace
from typing import Any, Dict, List, Tuple

from zeep import helpers

from . import AdapterError, OperationAdapter

__all__ = [
    "_GetCatalogoElectronicoByGLNAdapter",
]


class _GetCatalogoElectronicoByGLNAdapter(OperationAdapter):

    @classmethod
    def _name_mapping(_) -> Tuple[str, str]:
        return ("GET_CATALOGO_ELECTRONICO_BY_GLN", "getCatalogoElectronicoByGLN")

    def load(self, *args):
        try:
            return {
                # None,
                # None,
                "arg2": None if args[1] is None else int(args[1]),  # GLN / CUFE
                "arg3": args[2],  # CUIT
                "arg4": args[3],  # Descripción
                "arg5": None if args[4] is None else int(args[4]),  # ID Provincia
                "arg6": args[5],  # ID Tipo Agente
                "arg7": None if args[6] is None else int(args[6]),  # Número de página
                "arg8": (
                    None if args[7] is None else int(args[7])
                ),  # Cantidad de registros por página (máximo 100)
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
                    d["fecha_alta"] = (
                        None
                        if d["fecha_alta"] is None
                        else datetime.strptime(d["fecha_alta"], "%d/%m/%Y")
                        .date()
                        .strftime("%Y-%m-%d")
                    )
                    d["fecha_baja"] = (
                        None
                        if d["fecha_baja"] is None
                        else datetime.strptime(d["fecha_baja"], "%d/%m/%Y")
                        .date()
                        .strftime("%Y-%m-%d")
                    )
                    d["fecha_ult_modificacion"] = (
                        None
                        if d["fecha_ult_modificacion"] is None
                        else datetime.strptime(d["fecha_ult_modificacion"], "%d/%m/%Y")
                        .date()
                        .strftime("%Y-%m-%d")
                    )
                    d["id_localidad"] = (
                        None if d["id_localidad"] is None else int(d["id_localidad"])
                    )
                    d["id_provincia"] = (
                        None if d["id_provincia"] is None else int(d["id_provincia"])
                    )
                    d["id_tipo_agente"] = (
                        None if d["id_tipo_agente"] is None else int(d["id_tipo_agente"])
                    )
                    dumped.append(d)

                return dumped

            except ValueError as e:
                # this is an attemp to diferentiate of the ValueErrors in the request
                raise AdapterError(*e.args, code=418) from None

    @classmethod
    def _mock_data(cls, arg0, arg1, **kwargs):
        page_num = kwargs["arg7"]
        page_len = kwargs["arg8"]
        offset = (page_num - 1) * page_len
        page_data = cls._mock_data_[offset : offset + page_len]
        results = SimpleNamespace(list=page_data)
        return None if len(page_data) == 0 else results

    _mock_data_ = []
    _MOCK_ROW = {
        "codigo_postal": "0",
        "cuit": "glnws",
        "departamento": None,
        "direccion": "calle",
        "email": None,
        "entre_calle_1": None,
        "entre_calle_2": None,
        "fecha_alta": None,
        "fecha_baja": None,
        "fecha_ult_modificacion": None,
        "gln": "glnws",
        "gln_principal": None,
        "id_localidad": "1",
        "id_provincia": "1",
        "id_tipo_agente": "1",
        "nombre_localidad": "CIUDAD AUTONOMA DE BUENOS AIRES",
        "nombre_provincia": "CAPITAL FEDERAL",
        "nombre_tipo_agente": "LABORATORIO",
        "numero": None,
        "piso": None,
        "razon_social": "LABORATORIO",
        "razon_social_principal": None,
        "telefono": "glnws",
    }
    for n in range(260):
        row = _MOCK_ROW.copy()
        # row["_id_transaccion"] += n  # type: ignore
        _mock_data_.append(row)
