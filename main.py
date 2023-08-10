"""
This module provides examples on how to query the DB (Deutsche Bahn) api
"""

import datetime
import urllib3

from api import searchStationByName, bestPriceSearch, reconstruction, searchConnection

# - Hide warnings for insecure connections (proxy ;) )
#   TODO: Never use this in production
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STATION_ID_COLOGNE = 8000207
STATION_ID_FRANKFURT = 8000105


def sampleStationSearch():
    """Sample request for all train stations starting with 'Frank' """

    print("sampleStationSearch")

    # - request & response parsing
    matchingStationsRes = searchStationByName()
    matchingStations = [(station['name'], station['extId']) for station in matchingStationsRes['svcResL'][0]['res']['match']['locL']]

    print(*matchingStations, sep='\n')
    print("")


def sampleConnectionSearch():
    """Sample request for all connections from Frankfurt to Cologne on 20.05.2023"""

    print("sampleConnectionSearch")

    # - request & response parsing
    connectionsResponse = searchConnection()
    connections = [(connection['cid'], connection['ctxRecon']) for connection in connectionsResponse['svcResL'][0]['res']['outConL']]

    print(*connections, sep='\n')
    print("")


def sampleResonstruction():
    """
    Sample request for available ticket options (e.g. 'Sparpreis') for the connection:
        Frankfurt to Cologne from 25.05.2023 18:28-19:31 for ICE 10
    """

    print("sampleResonstruction")

    connectionPrices = reconstruction()
    ticket = [(ticket['fareL'][0]['name'], ticket['prc']) for ticket in connectionPrices['svcResL'][0]['res']['outConL'][0]['trfRes']['fareSetL']]

    print(*ticket, sep='\n')
    print("")


def sampleBestPriceSearch():
    """Sample request for best prices between Frankfurt -> Cologne"""

    print("sampleBestPriceSearch")
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    noon = 120000

    # - request & response parsing
    bestPriceResponse = bestPriceSearch(journeyDate=tomorrow, journeyTime=noon, departureStation=STATION_ID_FRANKFURT, arrivalStation=STATION_ID_COLOGNE)
    bestPrices = [(bestPrice['toTime'], bestPrice['bestPrice']['amount']) for bestPrice in bestPriceResponse['svcResL'][0]['res']['outDaySegL']]

    print(*bestPrices, sep='\n')
    print("")


def main():
    """ Demonstrate how to query various DB api endpoints """

    sampleStationSearch()
    sampleConnectionSearch()
    sampleResonstruction()
    sampleBestPriceSearch()


if __name__ == '__main__':
    main()
