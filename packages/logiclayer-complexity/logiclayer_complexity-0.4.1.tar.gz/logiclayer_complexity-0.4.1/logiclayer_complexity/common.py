from enum import Enum
from typing import List

import pandas as pd
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse, PlainTextResponse


class ResponseFormat(str, Enum):
    csv = "csv"
    jsonarrays = "jsonarrays"
    jsonrecords = "jsonrecords"
    tsv = "tsv"

    def serialize(self, df: pd.DataFrame) -> Response:
        headers = {
            "X-Tesseract-Columns": ",".join(df.columns),
            "X-Tesseract-RowCount": str(df.index.size),
        }

        if self is ResponseFormat.csv:
            return PlainTextResponse(
                df.to_csv(index=False, sep=","),
                headers=headers,
                media_type="text/csv",
            )

        if self is ResponseFormat.jsonarrays:
            res = df.to_dict("tight")
            return JSONResponse(
                {"headers": res["columns"], "data": res["data"]},
                headers=headers,
            )

        if self is ResponseFormat.jsonrecords:
            return JSONResponse(
                {"headers": tuple(df.columns), "data": df.to_dict("records")},
                headers=headers,
            )

        if self is ResponseFormat.tsv:
            return PlainTextResponse(
                df.to_csv(index=False, sep="\t"),
                headers=headers,
                media_type="text/tab-separated-values",
            )

        raise HTTPException(400, f"Invalid format type: {self.value}")


def split_dict(items: List[str], tokensep: str, keysep: str = ":"):
    """Splits the items in a list of strings to generate a set of (key, value) pairs."""
    return (
        tuple(item)
        for item in (
            token.split(keysep, maxsplit=1)
            for item in items
            for token in item.split(tokensep)
        )
    )


def series_compare(series: pd.Series, operator: str, value: int):
    """Applies the comparison operator against a scalar value over a pandas Series."""
    if operator == "lt":
        return series.lt(value)
    if operator == "lte":
        return series.le(value)
    if operator == "gt":
        return series.gt(value)
    if operator == "gte":
        return series.ge(value)
    if operator == "eq":
        return series.eq(value)
    if operator == "neq":
        return series.ne(value)

    raise ValueError(f"Invalid comparison operator '{operator}'")


def df_pivot(df: pd.DataFrame, *, index: str, column: str, value: str):
    """Pivots a DataFrame."""
    return (
        pd.pivot_table(df, index=[index], columns=[column], values=value)
        .reset_index()
        .set_index(index)
        .dropna(axis=1, how="all")
        .fillna(0)
        .astype(float)
    )


def df_melt(df: pd.DataFrame, *, index: str, value: str):
    """Unpivots a DataFrame. Adds category labels for the drilldown IDs."""
    df = (
        df.reset_index()
        .set_index(index)
        .dropna(axis=1, how="all")
        .fillna(0)
        .reset_index()
    )
    return pd.melt(df, id_vars=[index], value_name=value)
