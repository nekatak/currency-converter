import requests


class BaseClient(object):
    class ClientException(Exception):
        pass

    def __init__(self, url):
        self.url = url

    def get_xml(self):
        try:
            resp = requests.get(self.url)
            resp.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as e:
            raise BaseClient.ClientException(str(e))

        return resp.text


class YahooClient(BaseClient):

    YAHOO_FINANCE_EXCHANGE_RATES_URL = \
        "https://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote"

    def __init__(self):
        super().__init__(self.YAHOO_FINANCE_EXCHANGE_RATES_URL)


class ECBClient(BaseClient):

    ECB_EXCHANGE_RATES_URL = \
        "http://www.ecb.europa.eu/" \
        "stats/eurofxref/eurofxref-daily.xml?a1bf7a84cadc32c1dd25dbbb625566de"

    def __init__(self):
        super().__init__(self.ECB_EXCHANGE_RATES_URL)
