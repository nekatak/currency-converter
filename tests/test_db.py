import pytest

from db.model import conn, Rate


def setup_module(module):
    insstr = "INSERT INTO currencies VALUES (?, ?, ?)"
    currencies_set = (
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


def test_convert_from_currency_to_currency_without_date():
    insstr = "INSERT INTO currencies VALUES (?, ?, ?)"
    new_date_currency = (
        (6.9435, "BOB", "2017-11-04"),
    )
    conn.cursor().executemany(insstr, new_date_currency)
    conn.commit()

    conversion = Rate.convert_from_currency_to_currency(
        from_currency="USD", to_currenvcy="BOB"
    )

    assert conversion == 6.9435


def test_convert_from_To_non_existing_currency():
    with pytest.raises(Rate.ExchangeRateNotFound):
        Rate.convert_from_currency_to_currency(
            from_currency="APD", to_currenvcy="BOB", amount=250,
            date="2017-11-03"
        )


def test_save_or_update():
    curr = (1114.001, "KRW", "2017-11-03")
    rate = Rate(*curr)

    rate.save_to_db_or_update()

    get_from_db = conn.cursor().execute(
        "select exchange_rate from currencies where "
        "symbol = 'KRW'").fetchone()

    assert get_from_db is not None
    assert get_from_db[0] == 1114.001

    curr = (1116.001, "KRW", "2017-11-03")

    Rate(*curr).save_to_db_or_update()

    get_from_db = conn.cursor().execute(
        "select exchange_rate from currencies where "
        "symbol = 'KRW'").fetchone()

    assert get_from_db is not None
    assert get_from_db[0] == 1116.001
