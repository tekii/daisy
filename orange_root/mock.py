from datetime import datetime


def mock_data_f():
    # transaccionPlainWS
    _transaccionPlain = {
        "_d_evento": "ENVIO DE PRODUCTO EN CARACTER DEVOLUCION POR PROHIBICION",
        "_d_programa": None,
        "_f_evento": datetime.strptime("12/01/2024", "%d/%m/%Y").date().isoformat(),  # strftime("%Y-%m-d%"),
        "_f_transaccion": datetime.strptime("11/01/2024 16:17", "%d/%m/%Y %H:%M").isoformat(),
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
        "_vencimiento": datetime.strptime("07/01/2015", "%d/%m/%Y").date().isoformat(),
        "_ver2_paciente_apellido": None,
        "_ver2_paciente_documento": None,
        "_ver2_paciente_id_documento": None,
        "_ver2_paciente_id_obra_social": None,
        "_ver2_paciente_nombre": None,
        "_ver2_paciente_numero_afiliado": None,
    }
    _results = []
    _loop = 0
    while True:
        _ = _transaccionPlain.copy()
        _["_id_transaccion"] += _loop
        _results.append(_)
        _loop += 1
        if 460 == _loop:
            break
    #
    return _results


_mock_data = mock_data_f()


def mock_page(_, args):
    page_num = args[1]
    PAGE_LENGHT = 50
    start = (page_num - 1) * PAGE_LENGHT
    page_data = _mock_data[start : start + PAGE_LENGHT]
    return None if len(page_data) == 0 else page_data


def get_relay(operation):
    return mock_page


if __name__ == "__main__":
    toto = mock_page(1, _mock_data)
    toto = mock_page(2, _mock_data)
    toto = mock_page(3, _mock_data)
    toto = mock_page(4, _mock_data)
    toto = mock_page(5, _mock_data)
    toto = mock_page(6, _mock_data)
