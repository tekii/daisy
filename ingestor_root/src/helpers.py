"""Helpers for the BigQueryClient and credentials."""

import logging
from os import getenv
from sys import exit

from google.auth import default as default_credentials
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.bigquery import Client as BigQueryClient
from tekii.margot.toolbox.singleton import Singleton

__all__ = ["configuration"]


class _Configuration(object, metaclass=Singleton):

    def __init__(self) -> None:

        value = getenv("DATASET")
        if value is None:
            logging.fatal("DATASET is not defined.")
            exit(1)
        self._dataset: str = value

        value = getenv("SUBJECTS")
        if value is None:
            logging.fatal("SUBJECTS is not defined.")
            exit(1)
        else:
            self._subjects = value

        try:
            self._credentials, self._project = default_credentials()
            self._client = BigQueryClient(project=self._project, credentials=self._credentials)
        except DefaultCredentialsError as e:
            logging.fatal(f"Some problem  w/ credentials or the bigquery client {repr(e)}")
            exit(1)

    @property
    def PROJECT(self):
        """The active project id from credentials."""
        return self._project

    @property
    def DATASET(self):
        return self._dataset

    @property
    def SUBJECTS(self):
        return self._subjects

    @property
    def the_bq_client(self):
        return self._client

    @property
    def logger(self):
        return logging.getLogger("INGESTOR")


configuration = _Configuration()
