from typing import Any, Generator
from types import ModuleType
import pytest
from google.cloud import bigquery as bq


@pytest.fixture()
def the_history_module(test_runner_service_account_credentials) -> Generator[ModuleType, Any, None]:
    # remember, first monkeypatch the credentials, then import the module,
    # and i'm not sure if type annotate the return defeat the purpose
    # from google.auth import default as default_credentials
    import history

    # credentials, project = default_credentials()
    # client = bq.Client(project=project, credentials=credentials)
    # history.init(client, project)

    yield history
    del history


def test_table_creation(the_history_module):
    import history

    #
    table_name = the_history_module._TABLE + "_test"
    the_history_module._TABLE = table_name

    history.config.the_bq_client.delete_table(table=f"{history.config.PROJECT}.{history.config.DATASET}.{table_name}", not_found_ok=True)

    the_history_module.create_table(0)
    id = the_history_module.get_id()
    assert id is None

    history.config.the_bq_client.delete_table(table=f"{history.config.PROJECT}.{history.config.DATASET}.{table_name}", not_found_ok=False)


def test_save_id(the_history_module):
    import history

    table_name = the_history_module._TABLE
    # the_history_module._TABLE_NAME = table_name

    the_history_module.save_id(4255018)

    query = f"""SELECT id FROM `{history.config.PROJECT}.{history.config.DATASET}.{table_name}` WHERE id = @id LIMIT 10;"""
    job_config = bq.QueryJobConfig(query_parameters=[bq.ScalarQueryParameter("id", "INTEGER", 4255018)])
    results = history.config.the_bq_client.query_and_wait(
        query, job_config=job_config, project=history.config.PROJECT
    )  # Make an API request.

    assert 1 == results.total_rows

    id = the_history_module.get_id()
    assert id == 4255018


# def test_table_insert(the_test_client, the_ingest_module):
#    from datetime import datetime
#
#    credentials, project = the_test_client
#    client = bigquery.Client(project=project, credentials=credentials)
#
#    the_ingest_module.insert_attachment(client, project, 0, "aaaa", "q@a.b", datetime.now(), "test", "bbbb", "FILE.TXT")
