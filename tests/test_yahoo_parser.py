import types
import pytest

from parsers.yahoo_parser import YahooParser


@pytest.fixture
def yahoo_xml_report():
    with open("tests/fixtures/yahoo.xml", "r") as rf:
        return rf.read()


def test_parser(yahoo_xml_report):

    y_parser = YahooParser(yahoo_xml_report)

    gen = y_parser.get_rates_for_all_available_currencies()

    assert isinstance(gen, types.GeneratorType)

    rates = list(gen)
    assert rates[0].symbol == "KRW"
    assert rates[0].exchange_rate == 1114.790039
    assert rates[0].datetime == "2017-11-03T21:21:55+0000"
