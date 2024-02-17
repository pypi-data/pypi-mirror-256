"""Base functions to load data."""

from typing import Literal

import pandas

from llm_index.load import gcp


def load(
    project: str,
    source: Literal["gcp.bigquery", "gcp.storage"],
    query: str | None = None,
    file_path: str | None = None,
    bucket_name: str | None = None,
) -> pandas.DataFrame:
    if source == "gcp.bigquery":
        return gcp.bigquery.get_data(
            query=query,
            project=project,
        )

    if source == "gcp.storage":
        return gcp.storage.get_data(
            file_path=file_path, project=project, bucket_name=bucket_name
        )

    raise ValueError(
        "source should be equal to one of these values: gcp.bigquery, gcp.storage"
    )
