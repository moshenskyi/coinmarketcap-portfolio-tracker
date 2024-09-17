from typing import List

import requests
from pydantic import ValidationError

from models import QuoteListResponse


class CmcGateway:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url + 'cryptocurrency/quotes/latest'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

    def load(self, symbols: List[str]) -> QuoteListResponse:
        params = {
            'symbol': ','.join(symbols)
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)

        if response.status_code == 200:
            try:
                return QuoteListResponse(**response.json())
            except ValidationError as e:
                raise ValueError(f"Validation Error: {e}")
        else:
            raise ConnectionError(f"Failed to retrieve data: {response.status_code} {response.text}")
