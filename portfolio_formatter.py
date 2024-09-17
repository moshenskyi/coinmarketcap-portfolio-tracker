from typing import List

from tabulate import tabulate

from cmc_repository import CmcRepository


class PortfolioFormatter:
    def __init__(self, symbols: List[str], api: CmcRepository):
        self.symbols = symbols
        self.api = api

    def format(self):
        try:
            quotes = self.api.load(self.symbols)

            table_data = []
            for symbol, data in quotes.data.items():
                name = data.name
                price = data.quote['USD'].price
                percent_change_24h = data.quote['USD'].percent_change_24h
                table_data.append([name, symbol, f"${price:.2f}", f"{percent_change_24h:.2f}%"])

            headers = ["Name", "Symbol", "Price (USD)", "24h Change (%)"]
            print(tabulate(table_data, headers, tablefmt="pretty"))

        except ValueError as e:
            print(e)
        except ConnectionError as e:
            print(e)