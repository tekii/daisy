import pytest
from google.auth import default
from google.cloud.bigquery import Client


@pytest.fixture()
def the_history_module_and_stuff():
    import history

    _DATASET = "orange"
    #
    table_name = history._TABLE + "_test"
    history._TABLE = table_name

    credentials, project = default()
    client: Client = Client(credentials=credentials)
    client.delete_table(table=f"{project}.{_DATASET}.{table_name}", not_found_ok=True)

    yield history, _DATASET, credentials

    client.delete_table(table=f"{project}.{_DATASET}.{table_name}", not_found_ok=False)

    del history


def test_table_creation(the_history_module_and_stuff):

    history, dataset, credentials = the_history_module_and_stuff

    history_id = history.HistoryId(dataset=dataset, credentials=credentials)

    history_id.create_table(0)

    id = history_id.last_id

    assert id is not None and id == 0


def test_update_id(the_history_module_and_stuff):

    history, dataset, credentials = the_history_module_and_stuff

    history_id = history.HistoryId(dataset=dataset, credentials=credentials)

    history_id.create_table(0)

    id = history_id.last_id

    assert id is not None and id == 0

    history_id.last_id = 4255018

    assert history_id.last_id == 4255018
