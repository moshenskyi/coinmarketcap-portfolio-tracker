from typing import Dict

from pydantic import BaseModel


class QuoteModel(BaseModel):
    price: float
    percent_change_24h: float


class CurrencyModel(BaseModel):
    symbol: str
    name: str
    quote: Dict[str, QuoteModel]


class QuoteListResponse(BaseModel):
    data: Dict[str, CurrencyModel]
