class BaseParser():

    def get_parser_root(self):
        """gives the base element list in the xml document"""
        raise NotImplementedError()

    def get_rates_for_all_available_currencies(self):
        """generator that gives single Rate object that includes all
        info for single currency
        """
        raise NotImplementedError()
