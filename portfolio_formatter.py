from typing import Protocol, TypeVar, Dict, Any

from tabulate import tabulate

from models import CurrencyModel

T = TypeVar("T")


class Formatter(Protocol):
    def format(self, quotes: Dict[str, CurrencyModel]) -> T:
        ...


class TableFormatter(Formatter):
    def format(self, quotes: Dict[str, CurrencyModel]) -> str:
        try:
            table_data = []
            for symbol, data in quotes.items():
                name: str = data.name
                price: float = data.quote['USD'].price
                percent_change_24h: float = data.quote['USD'].percent_change_24h
                table_data.append([name, symbol, f"${price:.2f}", f"{percent_change_24h:.2f}%"])

            headers: list[str] = ["Name", "Symbol", "Price (USD)", "24h Change (%)"]
            return tabulate(table_data, headers, tablefmt="pretty")

        except ValueError as e:
            print(e)


class JinjaFormatter(Formatter):
    def format(self, quotes: Dict[str, CurrencyModel]) -> dict[Any, Any]:
        try:
            result = {}
            coins = []
            for symbol, data in quotes.items():
                name: str = data.name
                price: float = data.quote['USD'].price
                change: float = data.quote['USD'].percent_change_24h
                coins.append({
                    "name": name,
                    "symbol": symbol,
                    "price": f"${price:.5f}",
                    "change": f"{change:.2f}%"
                })

            result['coins'] = coins
            return result

        except ValueError as e:
            print(e)
