#
from typing import Any, Optional
import logging
from google.auth.credentials import Credentials
from google.cloud import bigquery as bq

__all__ = [
    "init",
    "create_table",
    "get_last_id",
    "save_new_id",
]


_logger = logging.getLogger("INGESTOR")
_project = None
_credentials: Credentials | None = None
_client: bq.Client | None = None


def init(project: Any | None = None, credentials: Credentials | None = None):
    #
    import google.auth

    global _project, _credentials, _client
    if credentials is None:
        _credentials, _project = google.auth.default()
    else:
        # untested
        _project = credentials.quota_project_id
        _credentials = credentials

    _client = bq.Client(project=_project, credentials=_credentials)


_DATASET = "orange"
_TABLE = "history"


def create_table(id) -> None:
    # Creates the table, this should not be run by an service account.
    # except the test-runner, any other lacks creation privileges and must fail.
    # TODO check if is actually the test-runner and fail gracefully.
    assert _client is not None

    query = f"""CREATE OR REPLACE TABLE `{_DATASET}.{_TABLE}` (id INTEGER NOT NULL); 
INSERT INTO `{_DATASET}.{_TABLE}` (id) VALUES (@id);"""
    job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("id", "INTEGER", id)])
    results = _client.query_and_wait(
        query,
        job_config=job_config,
        project=_project,
    )  # Make an API request.

    # if results.num_dml_affected_rows != 1:
    #    raise Exception


def get_id() -> int | None:
    # recover the id saved int the previus call
    assert _client is not None

    query = f"""SELECT id FROM `{_DATASET}.{_TABLE}` LIMIT 2;"""
    # job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("subject", "STRING", subject)])
    results = _client.query_and_wait(query, project=_project)  # Make an API request.
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
    assert _client is not None

    query = f"""UPDATE `{_DATASET}.{_TABLE}` SET id=@id WHERE TRUE;"""
    job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("id", "INTEGER", history_id)])
    results = _client.query_and_wait(
        query,
        job_config=job_config,
        project=_project,
    )  # Make an API request.
    if results.num_dml_affected_rows != 1:
        # TODO choose better exception
        raise Exception
