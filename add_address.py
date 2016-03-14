import os

from decouple import config

BASE_DIR = os.path.dirname(__file__)
GOOGLE_API_KEY = config('GOOGLE_API_KEY', default='')

# Making sure the correct request URL is set, according to
# the presence of the Google API key.
if GOOGLE_API_KEY is not None:
    BASE_URL = 'http://maps.google.com/maps/api/geocode/json?address={}&sensor=false&key={}'
else:
    BASE_URL = 'http://maps.google.com/maps/api/geocode/json?address={}&sensor=false&key={}'

def get_request_url(address):
    """
    Formats the request URL according to the presence
    of the Google API key.
    """
    if GOOGLE_API_KEY is None:
        return BASE_URL.format(address)
    return BASE_URL.format(address, GOOGLE_API_KEY)

def main():
    print(GOOGLE_API_KEY)

if __name__ == '__main__':
    main()
