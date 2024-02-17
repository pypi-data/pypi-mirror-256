import os

import pandas


def get_data(file_path: str) -> pandas.DataFrame:
    """Get data from disk."""
    if os.path.exists(file_path) is False:
        raise ValueError(f"file doesn't exist: {file_path}")

    extension = file_path.split(".")[-1]
    if extension == "json":
        return pandas.read_json(path_or_buf=file_path)

    if extension == "jsonl":
        return pandas.read_json(path_or_buf=file_path, lines=True)

    if extension == "parquet":
        return pandas.read_parquet(path=file_path)

    if extension == "csv":
        return pandas.read_csv(filepath_or_buffer=file_path)

    raise ValueError(f"file extension not handled: {extension}")
