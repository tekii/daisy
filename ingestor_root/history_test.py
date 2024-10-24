from typing import Any, Generator
from types import ModuleType
import pytest
from google.cloud import bigquery as bq


@pytest.fixture()
def the_history_module(test_runner_service_account_credentials) -> Generator[ModuleType, Any, None]:
    # remember, first monkeypatch the credentials, then import the module,
    # and i'm not sure if type annotate the return defeat the purpose
    import history

    history.init()
    yield history
    del history


def test_table_creation(the_history_module):
    #
    client: bq.Client = the_history_module._client  # type: ignore
    project = the_history_module._project
    dataset = the_history_module._DATASET
    table_name = the_history_module._TABLE + "_test"
    the_history_module._TABLE = table_name

    client.delete_table(table=f"{project}.{dataset}.{table_name}", not_found_ok=True)

    the_history_module.create_table(0)
    id = the_history_module.get_id()
    assert id is None

    client.delete_table(table=f"{project}.{dataset}.{table_name}", not_found_ok=False)


def test_table_creation2(the_history_module):
    the_history_module.create_table(0)


def test_save_id(the_history_module):

    client: bq.Client = the_history_module._client  # type: ignore
    project = the_history_module._project
    dataset = the_history_module._DATASET
    table_name = the_history_module._TABLE
    # the_history_module._TABLE_NAME = table_name

    the_history_module.save_id(4255018)

    query = f"""SELECT id FROM `{project}.{dataset}.{table_name}` WHERE id = @id LIMIT 10;"""
    job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("id", "INTEGER", 4255018)])
    results = client.query_and_wait(query, job_config=job_config, project=project)  # Make an API request.

    assert 1 == results.total_rows

    id = the_history_module.get_id()
    assert id == 4255018

    # id = the_history_module.get_id("dummy@margot.tekii.com.ar")
    # assert id is None


def test_table_insert(the_test_client, the_ingest_module):
    from google.cloud import bigquery
    from datetime import datetime

    credentials, project = the_test_client
    client = bigquery.Client(project=project, credentials=credentials)

    the_ingest_module.insert_attachment(client, project, 0, "aaaa", "q@a.b", datetime.now(), "test", "bbbb", "FILE.TXT")
