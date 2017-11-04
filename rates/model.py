class Rate(object):
    def __init__(self, exchange_rate, symbol, datetime):
        self.exchange_rate = exchange_rate
        self.symbol = symbol
        self.datetime = datetime

    def __repr__(self):
        return "%s exchange rate %s for %s" % (self.symbol, self.exchange_rate,
                                               self.date)
