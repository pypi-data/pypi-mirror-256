"""BigQuery data loader."""

import logging

import pandas
from google.cloud import bigquery


def get_data(query: str | None, project: str) -> pandas.DataFrame:
    """Get data from bigquery."""
    if query is None:
        raise ValueError("You need to set a sql query to run in BigQuery.")

    logging.info(f"load data from google cloud bigquery project={project}")
    client = bigquery.Client(project=project)
    return client.query(query=query).result().to_dataframe()
