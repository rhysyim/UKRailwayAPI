# UKRailwayAPI
REST API for retrieving railway data of England, Scotland and Wales

## Usage
### /code/[station name] - For station code with station name
```
/code/London Liverpool Street

{
"stationName": "London Liverpool Street", 
"code": "LST"
}
```
### /arrival/[station code] - For station arrivals with station code
```
/arrival/LST

[
{"time": "22:33", 
"destination": "London Paddington", 
"status": "On time", 
"platform": "B"
}, 
{"time": "22:39", 
"destination": "Abbey Wood", 
"status": "On time", 
"platform": "A"}
]

```

## Web Scraping Reference
National Rail - https://www.nationalrail.co.uk/

Wikipedia - UK Railway Stations - https://en.wikipedia.org/wiki/UK_railway_stations

## Modules and Packages
- Flask
- Flask RESTful
- Urllib
- Beautiful Soup
- Datetime
