#
from helpers import configuration as config
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter

__all__ = [
    "create_table",
    "get_last_id",
    "save_new_id",
]

_TABLE = "history"


def create_table(id) -> None:
    # Creates the table, this should not be run by an service account.
    # except the test-runner, any other lacks creation privileges and must fail.
    # TODO check if is actually the test-runner and fail gracefully.
    assert config.the_bq_client is not None

    query = f"""CREATE OR REPLACE TABLE `{config.DATASET}.{_TABLE}` (id INTEGER NOT NULL); 
INSERT INTO `{config.DATASET}.{_TABLE}` (id) VALUES (@id);"""
    job_config = QueryJobConfig(query_parameters=[ScalarQueryParameter("id", "INTEGER", id)])
    results = config.the_bq_client.query_and_wait(
        query,
        job_config=job_config,
        project=config.PROJECT,
    )  # Make an API request.

    # if results.num_dml_affected_rows != 1:
    #    raise Exception


def get_id() -> int | None:
    # recover the id saved int the previus call
    assert config.the_bq_client is not None

    query = f"""SELECT id FROM `{config.DATASET}.{_TABLE}` LIMIT 2;"""
    # job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("subject", "STRING", subject)])
    results = config.the_bq_client.query_and_wait(query, project=config.PROJECT)  # Make an API request.
    match results.total_rows:
        case 0:
            return None
        case 1:
            row = next(results)
            id = row.id
            return id if id > 0 else None
        case _:
            # TODO choose better exception
            raise Exception


def save_id(history_id: int) -> None:
    # save the new one
    assert config._client is not None

    query = f"""UPDATE `{config.DATASET}.{_TABLE}` SET id=@id WHERE TRUE;"""
    job_config = QueryJobConfig(query_parameters=[ScalarQueryParameter("id", "INTEGER", history_id)])
    results = config.the_bq_client.query_and_wait(
        query,
        job_config=job_config,
        project=config.PROJECT,
    )  # Make an API request.
    if results.num_dml_affected_rows != 1:
        # TODO choose better exception
        raise Exception
