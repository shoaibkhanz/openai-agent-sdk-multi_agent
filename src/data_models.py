from datetime import date as dt

import pandera.pandas as pa
from pandera.typing.pandas import Series


class InputTransactions(pa.DataFrameModel):
    date: Series[dt] = pa.Field(nullable=False)
    year: Series[int] = pa.Field(nullable=False, ge=1900, le=2026)
    month: Series[int] = pa.Field(nullable=False, ge=1, le=12)
    type: Series[str] = pa.Field(nullable=False, unique=False, isin=["credit", "debit"])
    category: Series[str] = pa.Field(nullable=False)
    amount: Series[float] = pa.Field(nullable=False)
    description: Series[str] = pa.Field(nullable=True)

    class Config:
        strict = True
        coerce = True
