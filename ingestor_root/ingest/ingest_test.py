# from typing import LiteralString
import pytest
from email.utils import parsedate_to_datetime
from io import StringIO
from google.cloud import bigquery as bq
from . import append_events_rows

project_id = "daisy-dev01"
table_name = "orange.append_events_rows_tests_2"


@pytest.fixture()
def mock_attachment_buffer():
    return StringIO(
        """07010779339704909921B03H076903     2025081300185824            20240918141277933970100207798138690004002300187193 000000000000250320240918
06000779339709065721MA003A         2025053100004943            202410070716779339701002020-21452470-9000400188336 000000000000028420241007SCHLENDER SESE, WALTER HEC
07010779339705124521FV038B         2025083100069330            20240918141277933970100207798169400023002300187191 000000000000291220240918
070107793397080122210024001719     2027022800221104            20240918141277933970100207798166490003002300187196 000000000000259220240918
"""
    )


@pytest.fixture()
def test_stuff():
    client = bq.Client(project=project_id)
    table_id = f"{project_id}.{table_name}"
    schema = [
        bq.SchemaField("evento", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("gtin", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("lote", field_type="STRING", mode="NULLABLE"),
        bq.SchemaField("vto", field_type="DATE", mode="NULLABLE"),
        bq.SchemaField("serie", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("evento_ts", field_type="DATETIME", mode="REQUIRED"),
        bq.SchemaField("origen", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("destino", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("remito", field_type="STRING", mode="NULLABLE"),
        bq.SchemaField("factura", field_type="STRING", mode="NULLABLE"),
        bq.SchemaField("codigo_cliente", field_type="STRING", mode="NULLABLE"),
        bq.SchemaField("evento_dia", field_type="DATE", mode="REQUIRED"),
        bq.SchemaField("nombre_agente", field_type="STRING", mode="NULLABLE"),
        #
        bq.SchemaField("history_id", field_type="INT64", mode="REQUIRED"),
        bq.SchemaField("message_id", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("message_from", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("message_date", field_type="TIMESTAMP", mode="REQUIRED"),
        bq.SchemaField("message_subject", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("attachment_id", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("filename", field_type="STRING", mode="REQUIRED"),
    ]
    table = bq.Table(table_id, schema=schema)
    table = client.create_table(table, exists_ok=True)

    yield (client, project_id, table_name)

    # client.delete_table(table, not_found_ok=True)
    pass


def test_event_07(mock_attachment_buffer, test_stuff) -> None:

    client, project_id, table_name = test_stuff

    append_events_rows(
        filepath_or_buffer=mock_attachment_buffer,
        destination_table=table_name,
        history_id=0,
        project_id=project_id,
        message_id="19233f063eec1719",
        message_from="a@b.c",
        message_date=parsedate_to_datetime("27 Sep 2024 11:43:58 -0300"),
        message_subject="the subject",
        attachment_id="ANGjdJ_deHe7fENfIhMS1GHfH2zZ_Lw66velytd13TEvoFpbUVsT_xdujKFOKcL0l3O0gwmW3ihl3zTn1n1gUcLmzV_UV6Y7JlWNKr42RYCEaH0W60gCj9Ml7h5SWnpjHpjOZCDGEsA4yAc3-RnyUP7YmVzPWvzttqghoFcSa2JIj04lJlu-HJnmYlP1HX-qN014vYR3UiwT7U5Y-su8pDpzRYAibzOyyzzvBD6I0BLJ3opG5Q0O6CCz7wa8gEpSDAzWDfppa_gh8s2Oo0LMkq67wmDNnV-IrSnMCI7HecChpFYvDVTBz_CiJSKQzvPP48QZKoNmUAAv6TTCeCOlcwCViIM7F3QfW7X87s-0xw7mj0i-puswnpj5cRCJH-MQdP_yKPe0_YgJwUY_brww",
        filename="TUTEUR2309240817.TXT",
    )
    # client = bq.Client(project=project_id)
    query = f"""SELECT * FROM `{project_id}.{table_name}` WHERE ORIGEN = @origen LIMIT 1000;"""
    job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("origen", "STRING", "7793397010020")])
    results = client.query_and_wait(query, job_config=job_config)  # Make an API request.
    assert 4 == results.total_rows
    pass
