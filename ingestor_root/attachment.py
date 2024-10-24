from typing import Any, Tuple, NamedTuple
from google.auth.credentials import Credentials
from google.cloud import bigquery as bq

__all__ = [
    "init",
    "create_table",
    "insert",
]

_project = None
_client: bq.Client | None = None

_DATASET = "orange"
_TABLE = "attachment"


def init():
    # TODO get the client as an argument
    import google.auth

    global _project, _client

    credentials, _project = google.auth.default()
    _client = bq.Client(project=_project, credentials=credentials)


def create_table():

    assert _client is not None

    schema = [
        bq.SchemaField("history_id", field_type="INTEGER", mode="REQUIRED"),
        bq.SchemaField("message_id", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("message_from", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("message_date", field_type="TIMESTAMP", mode="REQUIRED"),
        bq.SchemaField("message_subject", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("attachment_id", field_type="STRING", mode="REQUIRED"),
        bq.SchemaField("filename", field_type="STRING", mode="REQUIRED"),
    ]
    table = bq.Table(table_ref=f"{_project}.{_DATASET}.{_TABLE}", schema=schema)
    # table.time_partitioning = bq.TimePartitioning(
    #    field="message_date",
    #    type_=bq.TimePartitioningType.MONTH,
    #    require_partition_filter=False,
    # )
    table = _client.create_table(table, exists_ok=False)

    return table


def insert(row: Tuple):
    #
    assert _client is not None

    (
        history_id,
        message_id,
        message_from,
        message_date,
        message_subject,
        attachment_id,
        filename,
    ) = row

    query = f"""INSERT `{_DATASET}.{_TABLE}` (
history_id, message_id, message_from, message_date, message_subject, attachment_id, filename
) VALUES ( 
@history_id, @message_id, @message_from, @message_date, @message_subject, @attachment_id, @filename);"""
    job_config = bq.QueryJobConfig(
        query_parameters=[
            bq.ScalarQueryParameter("history_id", "INTEGER", history_id),
            bq.ScalarQueryParameter("message_id", "STRING", message_id),
            bq.ScalarQueryParameter("message_from", "STRING", message_from),
            bq.ScalarQueryParameter("message_date", "TIMESTAMP", message_date),
            bq.ScalarQueryParameter("message_subject", "STRING", message_subject),
            bq.ScalarQueryParameter("attachment_id", "STRING", attachment_id),
            bq.ScalarQueryParameter("filename", "STRING", filename),
        ]
    )
    results = _client.query_and_wait(query, job_config=job_config, project=_project)  # Make an API request.

    assert results.num_dml_affected_rows == 1
