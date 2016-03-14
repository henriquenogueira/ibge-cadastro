import os
from json import loads

from decouple import config

BASE_DIR = os.path.dirname(__file__)
BING_API_KEY = config('BING_API_KEY')

# Making sure the correct request URL is set, according to
# the presence of the Bing API key.
BASE_URL = 'http://dev.virtualearth.net/REST/v1/Locations?query={}&includeNeighborhood=0&include=queryParse,ciso2&maxResults=10&key={}'

def get_request_url(address):
    """
    Formats the request URL according to the presence
    of the Google API key.
    """
    if BING_API_KEY is None:
        return BASE_URL.format(address)
    return BASE_URL.format(address, BING_API_KEY)

def main():
    pass

if __name__ == '__main__':
    main()
