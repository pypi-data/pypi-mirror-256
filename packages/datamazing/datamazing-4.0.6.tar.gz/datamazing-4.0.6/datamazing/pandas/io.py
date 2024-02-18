from os import PathLike

import pandas as pd


def infer_iso_datetime(values: pd.Series) -> pd.Series:
    try:
        converted_values = pd.to_datetime(values)
    except (ValueError, TypeError):
        # if not possible to parse as datetime, return original values
        return values
    try:
        values_isoformat = converted_values.apply(pd.Timestamp.isoformat)
    except TypeError:
        return values
    if not (values_isoformat == values).all():
        # if original values is not in ISO 8601 format, return original values
        return values
    return converted_values


def infer_iso_timedelta(values: pd.Series) -> pd.Series:
    try:
        converted_values = pd.to_timedelta(values)
    except (ValueError, TypeError):
        # if not possible to parse as time delta, return original values
        return values
    try:
        values_isoformat = converted_values.apply(pd.Timedelta.isoformat)
    except TypeError:
        return values
    if not (values_isoformat == values).all():
        # if original values is not in ISO 8601 format, return original values
        return values
    return converted_values


def read_csv(filepath: PathLike) -> pd.DataFrame:
    """
    Read CSV into DataFrame. Datetimes and timedeltas in
    ISO 8601 format are inferred automatically.

    Args:
        filepath (str): Filepath of the CSV file
    """
    df = pd.read_csv(
        filepath,
        parse_dates=True,
        infer_datetime_format=True,
        keep_default_na=False,
        na_values=["nan"],
    )

    # try converting ISO 8601 strings to pd.Timestamp and pd.Timedelta
    df = df.apply(infer_iso_datetime)
    df = df.apply(infer_iso_timedelta)

    return df
