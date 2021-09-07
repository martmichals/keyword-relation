from . import scorer, scraper

class Manager:
    """ Class for the management of a large group of queries. Has options for
    both parallel and sequential processing of data sets.
    """

    def __init__(self, df, cores):
        """Initialize class, setting the data and number of cores on the machine

        Args:
            data (DataFrame): pandas dataframe, with columns ('keyword1', 'keyword2')
                              column values can be phrases or singular words
        """
        self.df = df
        self.cores = cores

    def say_hello():
        return 'hello'
