import treq
from twisted.internet import task, reactor, _sslverify
from twisted.internet.defer import inlineCallbacks
from twisted.web.http_headers import Headers
from twisted.web.client import getPage, readBody, Agent

_sslverify.platformTrust = lambda: None

URL = 'https://weatherapi-com.p.rapidapi.com/current.json?q='
headers = {
    'x-rapidapi-host': ['weatherapi-com.p.rapidapi.com'],
    'x-rapidapi-key': ['4767ff11ccmsh07e3f8226920ec0p1fb674jsn4711e7bb5020']
}


@inlineCallbacks  # working example from Zenpack SDK
def GetPage1():
    response = yield getPage('https://api.weather.gov/stations?state=OK')
    print (GetPage1.__name__)
    print response


@inlineCallbacks  # not working example
def GetPage2():
    response = yield getPage('https://weatherapi-com.p.rapidapi.com/current.json?q=Lviv', Headers(headers))
    print (GetPage2.__name__)
    print response


@inlineCallbacks  # working example
def AgentRequest():
    client = Agent(reactor)
    response = yield client.request('GET', 'https://weatherapi-com.p.rapidapi.com/current.json?q=Lviv',
                                    Headers(headers))
    data = yield readBody(response)
    print (AgentRequest.__name__)
    print data


@inlineCallbacks  # working example
def TreqGet():
    response = yield treq.get('https://weatherapi-com.p.rapidapi.com/current.json?q=Lviv', Headers(headers))
    data = yield treq.json_content(response)
    print (TreqGet.__name__)
    print data


def main():
    GetPage1()
    GetPage2()
    AgentRequest()
    TreqGet()
    
    reactor.run()


if __name__ == '__main__':
    main()
