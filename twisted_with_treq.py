import treq
import csv
import os

from twisted.internet import task, reactor, _sslverify
from twisted.web.http_headers import Headers

_sslverify.platformTrust = lambda: None

FILE = 'data.csv'
URL = 'https://weatherapi-com.p.rapidapi.com/current.json?q='
headers = {
    'x-rapidapi-host': ['weatherapi-com.p.rapidapi.com'],
    'x-rapidapi-key': ['4767ff11ccmsh07e3f8226920ec0p1fb674jsn4711e7bb5020']
}

INTERVAL = 30  # Time value after which the request will be repeated.


def fileEmptyOrNotExist(file):
    """
    Function that check, if file we needed exist
    :param file: str
    :return: True if file not exist or empty.
    """
    return not os.path.isfile(file) or os.path.getsize(file) == 0


def write_to_file(content):
    """
    Function that parse and print data into console and write it into file with appropriate headers.
    :param content: json
    :return: None
    """
    with open(FILE, 'a+') as f:
        fieldnames = [
            'gust_kph',
            'last_updated',
            'vis_miles',
            'pressure_in',
            'cloud',
            'precip_mm',
            'is_day',
            'feelslike_c',
            'feelslike_f',
            'wind_mph',
            'temp_f',
            'temp_c',
            'last_updated_epoch',
            'pressure_mb',
            'vis_km',
            'precip_in',
            'wind_dir',
            'wind_kph',
            'uv',
            'humidity',
            'gust_mph',
            'wind_degree'
        
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        print(content['current'])
        if fileEmptyOrNotExist(FILE):
            writer.writeheader()
        writer.writerow(content['current'])


def make_url(city):
    """
    Function that make unique URL for every city from basic URL and name of the city.
    :param city: str
    :return: URL: str
    """
    return URL + str(city)


def repeating_request(cities):
    """
    Function that send request and receive response from server via provided URL.
    :param cities: str
    :return: None
    """
    for city in cities:
        d = treq.get(make_url(city), Headers(headers))
        d.addCallback(treq.json_content)
        d.addCallback(write_to_file)


def main():
    cities = [  # List of cities we want to get info about.
        'Lviv',
        # 'Kiev',
        # 'Kirovohrad'
    ]
    
    repeating = task.LoopingCall(repeating_request, cities)
    repeating.start(INTERVAL)
    
    reactor.run()


if __name__ == '__main__':
    main()
