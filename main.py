import requests
import json


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


def main():
    # - fix search term, until checksum is calculated dynamically
    searchTerm = 'Frank'

    # - query api
    matchingStationsRes = searchStationByName(searchTerm)

    # - parse result
    matchingStations = [(station['name'], station['extId']) for station in
                        matchingStationsRes['svcResL'][0]['res']['match']['locL']]
    print(*matchingStations, sep='\n')


if __name__ == '__main__':
    main()
