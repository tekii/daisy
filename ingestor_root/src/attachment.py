from helpers import configuration as config
from inbox import AttachmentData
from google.cloud.bigquery import (
    Table,
    SchemaField,
    ScalarQueryParameter,
    QueryJobConfig,
)

__all__ = ["init", "create_table", "insert"]

_TABLE = "attachments"


def create_table():

    assert config.the_bq_client is not None

    schema = [
        SchemaField("history_id", field_type="INTEGER", mode="REQUIRED"),
        SchemaField("message_id", field_type="STRING", mode="REQUIRED"),
        SchemaField("message_from", field_type="STRING", mode="REQUIRED"),
        SchemaField("message_date", field_type="TIMESTAMP", mode="REQUIRED"),
        SchemaField("message_subject", field_type="STRING", mode="REQUIRED"),
        SchemaField("attachment_id", field_type="STRING", mode="REQUIRED"),
        SchemaField("filename", field_type="STRING", mode="REQUIRED"),
    ]
    table = Table(table_ref=f"{config.PROJECT}.{config.DATASET}.{_TABLE}", schema=schema)
    # table.time_partitioning = bq.TimePartitioning(
    #    field="message_date",
    #    type_=bq.TimePartitioningType.MONTH,
    #    require_partition_filter=False,
    # )
    table = config.the_bq_client.create_table(table, exists_ok=False)

    return table


def insert(row: AttachmentData):

    assert config.the_bq_client is not None

    query = f"""INSERT `{config.DATASET}.{_TABLE}` (
history_id, message_id, message_from, message_date, message_subject, attachment_id, filename
) VALUES ( 
@history_id, @message_id, @message_from, @message_date, @message_subject, @attachment_id, @filename);"""
    job_config = QueryJobConfig(
        query_parameters=[
            ScalarQueryParameter("history_id", "INTEGER", row.history_id),
            ScalarQueryParameter("message_id", "STRING", row.message_id),
            ScalarQueryParameter("message_from", "STRING", row.message_from),
            ScalarQueryParameter("message_date", "TIMESTAMP", row.message_date),
            ScalarQueryParameter("message_subject", "STRING", row.message_subject),
            ScalarQueryParameter("attachment_id", "STRING", row.attachment_id),
            ScalarQueryParameter("filename", "STRING", row.filename),
        ]
    )
    results = config.the_bq_client.query_and_wait(
        query,
        job_config=job_config,
        project=config.PROJECT,
    )  # Make an API request.

    assert results.num_dml_affected_rows == 1
