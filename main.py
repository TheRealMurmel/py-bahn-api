"""
This module provides examples on how to query the DB (Deutsche Bahn) api
"""

import requests
import json


def searchConnection(enableProxy=False):
    '''
    Search for connections between Köln and Frankfurt

    :param enableProxy:
    :return:
    '''

    if enableProxy:
        proxies = {'https': '0.0.0.0:8080'}
        verify = False
    else:
        proxies = {}
        verify = True

    url = "https://reiseauskunft.bahn.de/bin/mgate.exe"

    # - TODO: checksum calculation
    params = {
        'checksum': '42c706f5140e64354b22fc8f90dede07',
    }

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
                            "outDate": "20230520",
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

    response = requests.post(url, params=params, headers=headers, data=searchRequestEncoded, proxies=proxies, verify=verify)
    return response.json()


def searchStationByName(searchTerm, enableProxy=False):

    if searchTerm != 'Frank':
        raise Exception("Checksum is only valid for searchterm: 'Frank'")

    if enableProxy:
        proxies = {'https': '0.0.0.0:8080'}
        verify = False
    else:
        proxies = {}
        verify = True

    # - TODO: checksum calculation
    params = {
        'checksum': '5b2615acc349d757bc7c1d94da5e9ad3',
    }

    url = "https://reiseauskunft.bahn.de/bin/mgate.exe"
    headers = {
        "Host": "reiseauskunft.bahn.de",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; unknown Build/PI)",
        "Content-Type": "application/json;charset=UTF-8"
    }

    # - TODO: static auth token
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

    response = requests.post(url, params=params, headers=headers, data=searchRequestEncoded, proxies=proxies, verify=verify)

    return response.json()


def sampleStationSearch():
    """Search for all train stations matching starting with 'Frank' """

    # - fix search term, until checksum is calculated dynamically
    searchTerm = 'Frank'

    # - query api
    matchingStationsRes = searchStationByName(searchTerm)

    # - parse result
    matchingStations = [(station['name'], station['extId']) for station in
                        matchingStationsRes['svcResL'][0]['res']['match']['locL']]
    print(*matchingStations, sep='\n')


def sampleConnectionSearch():
    """Search for all connections from Frankfurt to Cologne on 20.05.2023"""
    connections = searchConnection()
    print(connections)


def main():
    """
    Showcase for station and connection search
    """
    sampleStationSearch()
    sampleConnectionSearch()


if __name__ == '__main__':
    main()
