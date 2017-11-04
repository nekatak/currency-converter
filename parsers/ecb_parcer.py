from parsers import BaseParser
from rates.model import Rate

import xml.etree.ElementTree as ET


class ECBParser(BaseParser):
    def __init__(self, xml_doc):
        self.xml_data = xml_doc
        self.parser_root = self.get_parser_root()
        self.usd_exchange_rate = self._get_usd_exchange_rate()

    def get_parser_root(self):
        return list(ET.fromstring(self.xml_data))[2]

    def _get_usd_exchange_rate(self):
        for child in self.parser_root[0]:
            if child.attrib['currency'] == "USD":
                return float(child.attrib['rate'])

    def _get_one_currency_rate_obj(self, child, date):

        return Rate(**{
            "symbol": child.attrib['currency'],
            "datetime": date,
            "exchange_rate": float(child.attrib['rate'])/self.usd_exchange_rate
        })

    def get_rates_for_all_available_currencies(self):
        date = self.parser_root[0].get("time") + "T16:00:00+0000"

        for child in self.parser_root[0]:
            yield self._get_one_currency_rate_obj(child, date)
