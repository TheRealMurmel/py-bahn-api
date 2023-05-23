# py-bahn-api
This project is a Proof of Concept for querying the DB (Deutsche Bahn) API.

## Features

* Search Stations
* Search Connections

## Requirements

Install the dependencies specified by the `requirements.txt`

## Run

```shell
$ python3 main.py

sampleStationSearch
('Frankfurt(Main)Hbf', '8000105')
('FRANKFURT(MAIN)', '8096021')
('Frankfurt(M)Flughafen', '8000281')
('Frankfurt(M) Flughafen Fernbf', '8070003')
('Frankenthal Hbf', '8000332')
('Frankfurt(Main)Süd', '8002041')
('Frankfurt(Oder)', '8010113')
('Frankfurt(Main)West', '8002042')
('Frankfurt-Niederrad', '8002050')
('Frankfurt-Höchst', '8000106')
('Frankfurt(M) Flughafen Regionalbf', '8070004')
('Frankfurt(M)Konstablerwache', '8004429')
('Frankenthal Süd', '8002025')
('Frankfurt(Main)Ost', '8002039')
('Frankfurt(M)Mühlberg', '8002034')
('Frankfurt-Mainkur', '8002048')
('Frankfurt(M)Galluswarte', '8006690')
('Frankfurt(M)Lokalbahnhof', '8002038')
('Frankenberg(Eder)', '8000104')
('Frankenthal-Flomersh', '8002014')
('Frankfurt-Sossenheim', '8002054')
('Frankfurt am Main - Stadion', '8002040')
('Frankfurt(M)Ostendstraße', '8002058')
('Frankfurt-Griesheim', '8002046')
('Frankfurt-Höchst Farbwerke', '8002051')

sampleConnectionSearch
('C-0', '011700')
('C-1', '014200')
('C-2', '013200')

sampleResonstruction
('Super Sparpreis', 7990)
('Sparpreis', 8790)
('Flexpreis', 8820)
('Flexpreis Plus', 10330)
('Super Sparpreis', 12390)

sampleBestPriceSearch
('070000', 1790)
('100000', 3190)
('130000', 3590)
('160000', 3590)
('190000', 3590)
('01000000', 2190)
```
