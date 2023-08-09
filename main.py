"""
This module provides examples on how to query the DB (Deutsche Bahn) api
"""

import datetime
from hashlib import md5
import json
import requests
import urllib3

# - Hide warnings for insecure connections (proxy ;) )
#   TODO: Never use this in production
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STATION_ID_COLOGNE = 8000207
STATION_ID_FRANKFURT = 8000105


def checksum(data):
    SALT = 'bdI8UVj40K5fvxwf'
    saltedData = data+SALT
    saltedDataEncoded = saltedData.encode('utf-8')
    return md5(saltedDataEncoded).hexdigest()


def searchConnection(journeyDate=20230821, enableProxy=False):
    """ Search for connections between Cologne and Frankfurt """

    if enableProxy:
        proxies = {'https': '0.0.0.0:8080'}
        verify = False
    else:
        proxies = {}
        verify = True

    url = "https://reiseauskunft.bahn.de/bin/mgate.exe"

    headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 3 Build/PI)",
                     "Content-Type": "application/json;charset=UTF-8"}
    searchRequest = {"auth": {"aid": "n91dB8Z77MLdoR0K", "type": "AID"},
                     "client": {"id": "DB", "name": "DB Navigator", "os": "Android 9", "res": "1080x2028", "type": "AND", "ua": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 3 Build/PI)", "v": 22080000},
                     "ext": "DB.R22.04.a",
                     "formatted": False,
                     "lang": "eng",
                     "svcReqL": [{
                        "cfg": {"polyEnc": "GPA", "rtMode": "HYBRID"},
                        "meth": "TripSearch",
                        "req": {
                            "outDate": f"{journeyDate}",
                            "outTime": "124900",
                            "arrLocL": [{
                                    "crd": {"x": 6959197, "y": 50942823}, "extId": "8000207",
                                    "lid": "A=1@O=Köln Hbf@X=6958730@Y=50943029@U=80@L=8000207@B=1@p=1683573667@",
                                    "name": "Köln Hbf",
                                    "type": "S"
                            }],
                            "depLocL": [{
                                "crd": {"x": 8663003, "y": 50106817},
                                "extId": "8000105",
                                "lid": "A=1@O=Frankfurt(Main)Hbf@X=8663785@Y=50107149@U=80@L=8000105@B=1@p=1683573667@",
                                "name": "Frankfurt(Main)Hbf", "type": "S"
                            }],
                            "getPasslist": True,
                            "getPolyline": True,
                            "jnyFltrL": [
                                {"mode": "BIT", "type": "PROD", "value": "11111111111111"}
                            ],
                            "trfReq": {"cType": "PK",
                                       "jnyCl": 2,
                                       "tvlrProf": [{
                                           "type": "E"}]
                                       }}
                     }],
                     "ver": "1.15"
                    }

    # - Server fails in case of unicode escape sequences
    #   hence, we have to handle the json serialization process
    #   in order to set `ensure_ascii`
    searchRequestStr = json.dumps(searchRequest, ensure_ascii=False, separators=(',', ':'))
    searchRequestEncoded = searchRequestStr.encode('utf-8')

    reqChecksum = checksum(searchRequestStr)
    params = {
        'checksum': f'{reqChecksum}',
    }

    response = requests.post(url, params=params, headers=headers, data=searchRequestEncoded, proxies=proxies, verify=verify)
    return response.json()


def searchStationByName(searchTerm='Frank', enableProxy=False):

    if enableProxy:
        proxies = {'https': '0.0.0.0:8080'}
        verify = False
    else:
        proxies = {}
        verify = True

    url = "https://reiseauskunft.bahn.de/bin/mgate.exe"

    headers = {
        "Host": "reiseauskunft.bahn.de",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; unknown Build/PI)",
        "Content-Type": "application/json;charset=UTF-8"
    }

    searchRequest = {"auth": {"aid": "n91dB8Z77MLdoR0K", "type": "AID"},
                     "client": {"id": "DB", "name": "DB Navigator", "os": "Android 9", "res": "1080x2028",
                                "type": "AND",
                                "ua": "Dalvik/2.1.0 (Linux; U; Android 9; unknown Build/PI)", "v": 22080000},
                     "ext": "DB.R22.04.a", "formatted": False, "lang": "eng", "svcReqL": [
            {"cfg": {"polyEnc": "GPA"},
             "meth": "LocMatch",
             "req": {
                 "input": {
                     "field": "S",
                     "loc":
                         {"name": f"{searchTerm}?"},
                     "maxLoc": 25
                 }
             }
             }],
                     "ver": "1.15"}

    # - Server fails in case of unicode escape sequences
    #   hence, we have to handle the json serialization process
    #   in order to set `ensure_ascii`
    searchRequestStr = json.dumps(searchRequest, ensure_ascii=False, separators=(',', ':'))
    searchRequestEncoded = searchRequestStr.encode('utf-8')

    reqChecksum = checksum(searchRequestStr)

    params = {
        'checksum': f'{reqChecksum}',
    }

    response = requests.post(url, params=params, headers=headers, data=searchRequestEncoded, proxies=proxies, verify=verify)

    return response.json()


def reconstruction(enableProxy=False):

    if enableProxy:
        proxies = {'https': '0.0.0.0:8080'}
        verify = False
    else:
        proxies = {}
        verify = True

    url = "https://reiseauskunft.bahn.de/bin/mgate.exe"

    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; unknown Build/PI)",
        "Content-Type": "application/json;charset=UTF-8"
    }

    reconstructionRequest = {
        "auth": {"aid": "n91dB8Z77MLdoR0K", "type": "AID"},
        "client": {"id": "DB", "name": "DB Navigator", "os": "Android 9", "res": "1080x2028", "type": "AND", "ua": "Dalvik/2.1.0 (Linux; U; Android 9; unknown Build/PI)", "v": 22080000},
        "ext": "DB.R22.04.a",
        "formatted": False,
        "lang": "eng",
        "svcReqL": [{
            "cfg": {"polyEnc": "GPA"},
            "meth": "Reconstruction",
            "req": {
                "getPasslist": True,
                "getPolyline": True,
                "outReconL": [{
                    "ctx": "T$A=1@O=Frankfurt(Main)Hbf@L=8000105@a=128@$A=1@O=Köln Hbf@L=8000207@a=128@$202308211326$202308211432$ICE  154$$1$$$$$$"
                }],
                "trfReq": {
                    "cType": "PK",
                    "directESuiteCall": True,
                    "jnyCl": 2,
                    "rType": "DB-PE",
                    "tvlrProf": [{"type": "E"}]
                }
            }
        }],
        "ver": "1.15"
    }

    # - Server fails in case of unicode escape sequences
    #   hence, we have to handle the json serialization process
    #   in order to set `ensure_ascii`
    reconstructionRequestStr = json.dumps(reconstructionRequest, ensure_ascii=False, separators=(',', ':'))
    reconstructionRequestEncoded = reconstructionRequestStr.encode('utf-8')

    requestChecksum = checksum(reconstructionRequestStr)

    params = {
        'checksum': f'{requestChecksum}',
    }

    response = requests.post(url, params=params, headers=headers, data=reconstructionRequestEncoded, proxies=proxies, verify=verify)
    return response.json()


def bestPriceSearch(journeyDate, journeyTime=120000, departureStation=STATION_ID_FRANKFURT, arrivalStation=STATION_ID_COLOGNE, enableProxy=False):

    if enableProxy:
        proxies = {'https': '0.0.0.0:8080'}
        verify = False
    else:
        proxies = {}
        verify = True

    url = "https://reiseauskunft.bahn.de/bin/mgate.exe"

    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 3 Build/PI)",
        "Content-Type": "application/json;charset=UTF-8"
        }

    bestPriceSearchRequest = {
        "auth": {"aid": "n91dB8Z77MLdoR0K", "type": "AID"},
        "client": {"id": "DB", "name": "DB Navigator", "os": "Android 9", "res": "1080x2028", "type": "AND", "ua": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 3 Build/PI)", "v": 22080000},
        "ext": "DB.R22.04.a",
        "formatted": False,
        "lang": "eng",
        "svcReqL": [{
            "cfg": {"polyEnc": "GPA", "rtMode": "HYBRID"},
            "meth": "BestPriceSearch",
            "req": {
                "outDate": f"{journeyDate}",
                "outTime": f"{journeyTime}",
                "depLocL": [{
                    "extId": f"{departureStation}",
                    "type": "S"
                }],
                "arrLocL": [
                    {
                        "extId": f"{arrivalStation}",
                        "type": "S"
                    }],
                "getPasslist": True,
                "getPolyline": True,
                "jnyFltrL": [{
                    "mode": "BIT",
                    "type": "PROD",
                    "value": "11111111111111"
                }],
                "trfReq": {
                    "cType": "PK",
                    "jnyCl": 2,
                    "tvlrProf": [{"type": "E"}]
                }
            }
        }],
        "ver": "1.15"
    }

    # - Server fails in case of unicode escape sequences
    #   hence, we have to handle the json serialization process
    #   in order to set `ensure_ascii`
    bestPriceSearchRequestStr = json.dumps(bestPriceSearchRequest, ensure_ascii=False, separators=(',', ':'))
    bestPriceSearchRequestEncoded = bestPriceSearchRequestStr.encode('utf-8')

    reqChecksum = checksum(bestPriceSearchRequestStr)

    params = {
        'checksum': reqChecksum,
    }

    response = requests.post(url, params=params, headers=headers, data=bestPriceSearchRequestEncoded, proxies=proxies, verify=verify)
    return response.json()


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
