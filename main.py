import os

import yaml
from dotenv import load_dotenv

from cmc_repository import CmcRepository
from portfolio_formatter import PortfolioFormatter


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
    base_url = config['base_url']
    preselected_symbols = config['preselected_symbols']

    load_dotenv()
    api_key = os.getenv('cmc_api_key')

    repository = CmcRepository(api_key, base_url)
    portfolio_display = PortfolioFormatter(preselected_symbols, repository)
    portfolio_display.format()


if __name__ == "__main__":
    main()
