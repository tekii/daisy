from google.cloud.bigquery import Client, QueryJobConfig, ScalarQueryParameter

# from tekii.margot.toolbox.singleton import Singleton


__all__ = ["HistoryId"]

_TABLE = "history_id"


class HistoryId:  # , metaclass=Singleton):
    """Last Gmail History ID"""

    def __init__(self, dataset: str, credentials):
        self._DATASET = dataset
        self._client: Client = Client(credentials=credentials)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._client.__exit__(exc_type, exc_value, traceback)

    def create_table(self, id) -> None:
        # Creates the table, this should not be run by an service account.
        # except the test-runner, any other lacks creation privileges and must fail.
        # TODO check if is actually the test-runner and fail gracefully.
        query = f"""CREATE OR REPLACE TABLE `{self._DATASET}.{_TABLE}` (id INTEGER NOT NULL);
            INSERT INTO `{self._DATASET}.{_TABLE}` (id) VALUES (@id);"""
        job_config = QueryJobConfig(query_parameters=[ScalarQueryParameter("id", "INTEGER", id)])
        results = self._client.query_and_wait(
            query,
            job_config=job_config,
        )  # Make an API request.

        # if results.num_dml_affected_rows != 1:
        #    raise Exception

    @property
    def last_id(self) -> int:
        query = f"""SELECT id FROM `{self._DATASET}.{_TABLE}` LIMIT 2;"""
        # job_config = bq.QueryJobConfig(
        # query_parameters=[bq.ScalarQueryParameter("subject", "STRING", subject)])
        results = self._client.query_and_wait(query)  # Make an API request.
        match results.total_rows:
            case 0:
                raise Exception
            case 1:
                row = next(results)
                id = row.id
                return id  # if id > 0 else None
            case _:
                # TODO choose better exception
                raise Exception("HistoryId multiple results")

    @last_id.setter
    def last_id(self, value: int):

        query = f"""UPDATE `{self._DATASET}.{_TABLE}` SET id=@id WHERE TRUE;"""
        job_config = QueryJobConfig(
            query_parameters=[ScalarQueryParameter("id", "INTEGER", value=value)]
        )

        results = self._client.query_and_wait(
            query,
            job_config=job_config,
        )  # Make an API request.
        if results.num_dml_affected_rows != 1:
            # TODO choose better exception
            raise Exception("HistoryId multiple results")
