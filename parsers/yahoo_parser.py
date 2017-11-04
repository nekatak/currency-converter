from parsers import BaseParser
from rates.rate_model import Rate

import xml.etree.ElementTree as ET

class YahooParser(BaseParser):
    def __init__(self, xmldoc):
        self.xml_data = xmldoc
        self.parser_root = self.get_parser_root()

    def get_parser_root(self):

        return list(ET.fromstring(self.xml_data))[1]

    def _get_one_currency_rate_obj(self, resource):
        for node in resource.findall("field"):
            element_name = node.get("name")
            if element_name == "name":
                if not node.text.startswith("USD"):
                    return {}
                symbol = node.text[4::]
            if element_name == "price":
                exchange_rate = float(node.text)
            if element_name == "utctime":
                datetime = node.text

        return Rate(**{
            "symbol": symbol,
            "exchange_rate": exchange_rate,
            "datetime": datetime,
        })


    def get_rates_for_all_available_currencies(self):
        for resource in self.parser_root.findall("resource"):
            for node in resource.findall("field"):
                yield self._get_currency_rate_obj(node)
