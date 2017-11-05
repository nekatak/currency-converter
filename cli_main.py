import argparse

from db.model import Rate
from clients.clients import BaseClient, YahooClient, ECBClient
from parsers.ecb_parcer import ECBParser
from parsers.yahoo_parser import YahooParser


SUPPORTED_CURRENCIES = (
    "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK",
    "CHF", "NOK", "HRK", "RUB", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD",
    "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB",
    "ZAR",
)

def get_conversion_from_db(args):
    argums = [args.fromcurrency, args.tocurrency]
    if args.amount:
        argums.append(args.amount)

    return Rate.convert_from_currency_to_currency(*argums)

def get_rates_and_save_in_db(client, XMLParser):
    xml = client().get_xml()
    xmlparser = XMLParser(xml)
    rates = xmlparser.get_rates_for_all_available_currencies()

    for rate in rates:
        rate.save_to_db_or_update()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Convert amount from a currency to another. Supported currencies: " +
        ", ".join(SUPPORTED_CURRENCIES)
    )
    parser.add_argument("--fromcurrency", type=str)
    parser.add_argument("--tocurrency", type=str)
    parser.add_argument(
        "--amount", type=int,
        help="amount to be converted from_currency to to_currency")

    args = parser.parse_args()

    if args.fromcurrency not in SUPPORTED_CURRENCIES or \
                    args.tocurrency not in SUPPORTED_CURRENCIES:
        raise IOError("Bad input...")

    try:
        print(get_conversion_from_db(args))
        exit(0)
    except Rate.ExchangeRateNotFound:
        pass

    try:
        get_rates_and_save_in_db(YahooClient, YahooParser)
    except BaseClient.ClientException as e:
        print(str(e))
        try:
            get_rates_and_save_in_db(ECBClient, ECBParser)
        except BaseClient.ClientException as e:
            print(e)
            exit(1)

    print(get_conversion_from_db(args))
    exit(0)