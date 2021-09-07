import requests, json, re
from boilerpipe.extract import Extractor

"""Assortment of functions for web scraping using keyword pairings.
"""
class Scraper:
    def __init__(self, key):
        """Initialize the web scraper with an API key.

        Args:
            key (str): API key for the USearch API
        """
        self.bing_key = key

    def get_links_for_pair(self, k1, k2):
        """Get webpage links for a particular keyword pairing.

        Args:
            k1 (str): first keyword
            k2 (str): second keyword

        Returns:
            links ([list): a list of urls resulting from the web search. Empty list
                in the case that no web pages were found.
        """

        # Set up and launch API request
        url = "https://api.bing.microsoft.com/v7.0/search"
        params = {
            'q': '\"{}\" \"{}\"'.format(k1, k2),
            'count': '50'
        }
        headers = {
            'Ocp-Apim-Subscription-Key': self.bing_key,
        }
        response = requests.request('GET', url, headers=headers, params=params)

        # Check status code
        if response.status_code != 200:
            return []

        # Parse the response
        results = json.loads(response.text)

        # Check result count
        if results['webPages']['totalEstimatedMatches'] == 0:
            return []

        # Parse json return to generate a list of links to scrape
        return [result['url'] for result in results['webPages']['value']]

    def get_natural_text(self, url):
        # Extract natural language from the passed webpage
        #   Methods employed in the implementation are described in this paper:
        #   http://www.l3s.de/~kohlschuetter/publications/wsdm187-kohlschuetter.pdf
        try:
            extractor = Extractor(extractor='DefaultExtractor', url=url)
            return extractor.getText()
        except Exception as e:
            print('An exception occured!')
            return ''

