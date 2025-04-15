#
"""Helpers for the BigQueryClient and credentials.
"""
from os import getenv
from sys import exit
import logging

from google.auth import default as default_credentials
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.bigquery import Client as BigQueryClient

__all__ = ["configuration"]

_logger = logging.getLogger("INGESTOR")


class Singleton(type):

    def __call__(cls, *args, **kwargs):
        if cls._the_instance is None:
            instance = cls.__new__(cls, *args, **kwargs)
            instance.__init__(*args, **kwargs)
            cls._the_instance = instance
        else:
            instance = cls._the_instance
        return instance

    def __new__(cls, name, bases, dct):
        instance = super().__new__(cls, name, bases, dct)
        # add the class variable to store the instance
        instance._the_instance = None
        return instance

    # def __init__(cls, name, bases, dct):
    #    pass


class _Configuration(object, metaclass=Singleton):

    def __init__(self) -> None:

        value = getenv("DATASET")
        if value is None:
            _logger.fatal("DATASET is not defined.")
            exit(1)
        self._dataset: str = value

        value = getenv("SUBJECTS")
        if value is None:
            _logger.fatal("SUBJECTS is not defined.")
            exit(1)
        else:
            self._subjects = value

        try:
            self._credentials, self._project = default_credentials()
            self._client = BigQueryClient(project=self._project, credentials=self._credentials)
        except DefaultCredentialsError as e:
            _logger.fatal(f"Some problem  w/ credentials or the bigquery client {repr(e)}")
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
