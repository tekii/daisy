""" """

from email.utils import parsedate_to_datetime
import pandas as pd
import pandas_gbq  # type: ignore[import-untyped]

__all__ = ["append_events_rows"]


def append_events_rows(
    filepath_or_buffer,
    destination_table,
    message_id: str,
    message_date: str,
    attach_id: str,
    filename: str,
    start_history_id: str,
    project_id=None,
):
    r"""
    Read the movimientos file into a Dataframe and append them to the bq table
    """

    def to_datetime(cell):
        return pd.to_datetime(cell, format="%Y%m%d%H%M")

    def to_datetime_or_None(cell):
        return pd.to_datetime(cell, format="%Y%m%d") if cell != "00000000" else None

    def to_comprobante_or_None(cell):
        return cell if cell != "000000000000" else None

    def to_clientcode_or_None(cell):
        return cell if cell != "0000" else None

    def to_str(cell):
        return str(cell)

    # read the file
    df = pd.read_fwf(
        filepath_or_buffer=filepath_or_buffer,
        names=[
            "evento",
            "_1",
            "gtin",
            "_2",
            "lote",
            "vto",
            "serie",
            "evento_ts",
            "origen",
            "destino",
            "remito",
            "_3",
            "factura",
            "codigo_cliente",
            "evento_dia",
        ],
        widths=[
            2,  # MOVI
            2,  # DUMMY
            14,  # GTIN
            2,  # DUMMY
            15,  # LOTE
            8,  # VTO
            20,  # SERIE
            12,  # FECHA HORA
            13,  # ORIGEN
            13,  # DESTINO
            12,  # REMITO
            1,  # LETRA
            12,  # FACTURA
            4,  # CLIENTE
            8,  # DIA
        ],
        converters={
            "evento": to_str,
            "gtin": to_str,
            "lote": to_str,
            "vto": to_datetime_or_None,
            "serie": to_str,
            "evento_ts": to_datetime,
            "origen": to_str,
            "destino": to_str,
            "remito": to_comprobante_or_None,
            "factura": to_comprobante_or_None,
            "codigo_cliente": to_clientcode_or_None,
            "evento_dia": to_datetime_or_None,
        },
        skip_blank_lines=True,
    )

    # delete unused
    df.drop(columns=["_1", "_2", "_3"], inplace=True)

    # add start_history_id
    assert start_history_id is not None
    df.insert(12, "start_history_id", start_history_id)

    # add metadata
    assert message_id is not None
    df.insert(13, "message_id", message_id)

    assert message_date is not None
    dt = parsedate_to_datetime(message_date)
    df.insert(14, "message_date", dt)

    assert attach_id is not None
    df.insert(15, "attach_id", attach_id)

    assert filename is not None
    df.insert(16, "filename", filename)
    #
    pandas_gbq.to_gbq(
        dataframe=df,
        destination_table=destination_table,
        project_id=project_id,
        if_exists="append",
        #        table_schema=[
        #            {"name": "evento", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "gtin", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "lote", "type": "STRING", "mode": "NULLABLE"},
        #            {"name": "vto", "type": "DATE", "mode": "NULLABLE"},
        #            {"name": "serie", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "evento_ts", "type": "DATETIME"},
        #            {"name": "origen", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "destino", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "remito", "type": "STRING", "mode": "NULLABLE"},
        #            {"name": "factura", "type": "STRING", "mode": "NULLABLE"},
        #            {"name": "codigo_cliente", "type": "STRING", "mode": "NULLABLE"},
        #            {"name": "evento_dia", "type": "DATE", "mode": "REQUIRED"},
        #            {"name": "start_history_id", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "message_id", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "message_date", "type": "TIMESTAMP", "mode": "REQUIRED"},
        #            {"name": "attach_id", "type": "STRING", "mode": "REQUIRED"},
        #            {"name": "filename", "type": "STRING", "mode": "REQUIRED"},
        #        ],
        progress_bar=False,
    )
