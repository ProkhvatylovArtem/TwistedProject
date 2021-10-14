import treq
from twisted.internet import task, reactor
from datetime import datetime

FILE = 'data.csv'
URL = 'http://dataservice.accuweather.com/currentconditions/v1/'
API_KEY = '/?apikey=OfuODmknhtgNGGBzMiNCm2yaEfAnCqxI'
INTERVAL = 30


def write_to_file(content):
    with open(FILE, 'ab') as f:
        f.write('Time of the request: {0}\n{1}\n '.format(str(datetime.now()), content))
    print('Time of the request: {0}\n{1}\n '.format(str(datetime.now()), content))


def make_url(city_key):
    return URL + str(city_key) + API_KEY


def repeating_request(cities):
    for city in dict(cities).values():
        d = treq.get(make_url(city))
        d.addCallback(treq.content)
        d.addCallback(write_to_file)


def main():
    cities = {
        'Lviv': '324561',
        'Kyiv': '324505',
        'Kropyvnytskyi': '324291'
    }
    
    repeating = task.LoopingCall(repeating_request, cities)
    repeating.start(INTERVAL)
    
    reactor.run()


if __name__ == '__main__':
    main()
