from typing import List, Protocol

from tabulate import tabulate

from cmc_gateway import CmcGateway

class Formatter(Protocol):
    def format(self):
        ...


class PortfolioFormatter(Formatter):
    def __init__(self, symbols: List[str], api: CmcGateway):
        self.symbols = symbols
        self.api = api

    def format(self):
        try:
            quotes = self.api.load(self.symbols)

            table_data = []
            for symbol, data in quotes.data.items():
                name: str = data.name
                price: float = data.quote['USD'].price
                percent_change_24h: float = data.quote['USD'].percent_change_24h
                table_data.append([name, symbol, f"${price:.2f}", f"{percent_change_24h:.2f}%"])

            headers: list[str] = ["Name", "Symbol", "Price (USD)", "24h Change (%)"]
            print(tabulate(table_data, headers, tablefmt="pretty"))

        except ValueError as e:
            print(e)
        except ConnectionError as e:
            print(e)