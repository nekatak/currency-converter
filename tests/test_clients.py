from clients.clients import YahooClient, ECBClient


def test_ecb_client():
    assert ECBClient().get_xml()


def test_yahoo_client():
    assert YahooClient().get_xml()