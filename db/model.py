import datetime
import sqlite3

conn = sqlite3.connect("currencies.db")


class Rate(object):
    class ExchangeRateNotFound(Exception):
        pass

    def __init__(self, exchange_rate, symbol, date):
        self.exchange_rate = exchange_rate
        self.symbol = symbol
        self.date = date

    def __repr__(self):
        return "%s exchange rate %s for %s" % (self.symbol, self.exchange_rate,
                                               self.date)

    def save_to_db_or_update(self):
        c = conn.cursor()
        selstr = "SELECT * FROM currencies where symbol = '%s' "\
            "and date = '%s'" % (self.symbol, self.date)
        find_todays_curr = c.execute(selstr).fetchone()

        if find_todays_curr is None:
            insstr = "INSERT INTO currencies VALUES ('%s', '%s', '%s')" % (
                self.exchange_rate, self.symbol, self.date)
        else:
            insstr = "UPDATE currencies SET exchange_rate=%s " \
                "WHERE symbol = '%s' and date = '%s'" % (
                self.exchange_rate, self.symbol, self.date,)

        c.execute(insstr)
        conn.commit()

    @classmethod
    def convert_from_currency_to_currency(cls, from_currency,
                                          to_currenvcy, amount=1, date=None):
        date = date or str(datetime.date.today() - datetime.timedelta(days=1))
        selstr = "select exchange_rate from currencies where symbol ='%s' and"\
        " date = '{}'".format(date)

        from_currency_exch_rate = to_currenvcy_exch_rate = None

        if from_currency == "USD":
            from_currency_exch_rate = [1.00,]
        else:
            c = conn.cursor()
            from_currency_exch_rate = c.execute(selstr % from_currency).fetchone()

        if to_currenvcy == "USD":
            to_currenvcy_exch_rate = [1.00,]
        else:
            to_currenvcy_exch_rate = c.execute(selstr % to_currenvcy).fetchone()

        if from_currency_exch_rate is None or to_currenvcy_exch_rate is None:
            raise cls.ExchangeRateNotFound()

        return amount * to_currenvcy_exch_rate[0] / from_currency_exch_rate[0]
