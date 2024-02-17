import os
import logging

import pandas
import google.cloud.storage as storage

import llm_index.load.local.base


def get_data(
    file_path: str | None, bucket_name: str | None, project: str
) -> pandas.DataFrame:
    """Get data from google cloud storage."""
    if file_path is None:
        raise ValueError("You need to set the file path.")

    if bucket_name is None:
        raise ValueError("You need to set the bucket name.")

    logging.info(
        f"load data from google cloud storage file_path={file_path} bucket_name={bucket_name} project={project}"
    )

    file_name = file_path.split("/")[-1]
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=file_path)
    blob.download_to_filename(filename=file_name)
    output = llm_index.load.local.base.get_data(file_path=file_path)
    os.remove(file_name)
    return output
