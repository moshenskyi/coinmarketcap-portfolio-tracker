import os

import yaml
from dotenv import load_dotenv

from cmc_gateway import CmcGateway
from portfolio_formatter import PortfolioFormatter, Formatter
from sender import EmailSender, Sender


def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    # Parse the API key, base URL, and preselected symbols from the config
    base_url = config['api']['base_url']
    preselected_symbols = config['api']['preselected_symbols']

    return {
        'base_url': base_url,
        'preselected_symbols': preselected_symbols
    }


def main():
    config = load_config('config.yaml')
    base_url: str = config['base_url']
    preselected_symbols: list[str] = config['preselected_symbols']

    load_dotenv()
    api_key: str = os.getenv('cmc_api_key')

    cmc_gateway: CmcGateway = CmcGateway(api_key, base_url)
    portfolio_display: Formatter = PortfolioFormatter(preselected_symbols, cmc_gateway)

    formatted_data = portfolio_display.format()
    sender: Sender = EmailSender()
    sender.send(formatted_data)


if __name__ == "__main__":
    main()
