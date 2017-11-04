import pytest

from db.model import conn, Rate


def setup_module(module):
    insstr = "INSERT INTO currencies VALUES (?, ?, ?)"
    currencies_set = (
        (1114.001, "KRW", "2017-11-03"),
        (22699.301, "VND", "2017-11-03"),
        (6.860000, "BOB", "2017-11-03"),
    )
    c = conn.cursor()
    c.executemany(insstr, currencies_set)
    conn.commit()


def teardown_module(module):
    conn.cursor().execute("DELETE FROM currencies")
    conn.commit()


def test_convert_from_curr_to_currency():
    conversion = Rate.convert_from_currency_to_currency(
        from_currency="VND", to_currenvcy="BOB", amount=250,
        date="2017-11-03"
    )
    assert conversion == 250 * 6.860000 / 22699.301

def test_convert_from_To_non_existing_currency():
    with pytest.raises(Rate.ExchangeRateNotFound):
        Rate.convert_from_currency_to_currency(
            from_currency="APD", to_currenvcy="BOB", amount=250,
            date="2017-11-03"
        )
