# UKRailwayAPI
REST API for retrieving railway data of England, Scotland and Wales

## Usage
### Base URL
https://uk-railway-api.rhysyim.repl.co
### /code/[station name] - For station code with station name
```
https://uk-railway-api.rhysyim.repl.co/code/London Liverpool Street

{
  "stationName": "London Liverpool Street",
  "code": "LST"
}
```
### /arrival/[station code] - For station arrivals with station code
```
https://uk-railway-api.rhysyim.repl.co/arrival/LST

[
  {
    "time": "22:33",
    "destination": "London Paddington",
    "status": "On time",
    "platform": "B"
  },
  {
    "time": "22:39",
    "destination": "Abbey Wood",
    "status": "On time",
    "platform": "A"
  }
]
```
### /history/[departureStation]/[arrivalStation]/[date] - Train arrival history for 6 months
```
https://uk-railway-api.rhysyim.repl.co/history/London+Liverpool+Street+(LST)/London+Paddington+(PAD)/01-12-2022

[
  {
    "operator": "XR",
    "departureStation": "London Liverpool Street (LST)",
    "arrivalStation": "London Paddington (PAD)",
    "scheduledDeparture": "06:12",
    "scheduledArrival": "06:23",
    "duration": "11m",
    "actualArrival": "06:23",
    "late": 0
  }
]
```

## Web Scraping Reference
National Rail - https://www.nationalrail.co.uk/

Wikipedia - UK Railway Stations - https://en.wikipedia.org/wiki/UK_railway_stations

Recent Train Times - https://www.recenttraintimes.co.uk

## Modules and Packages
- Flask
- Flask RESTful
- Urllib
- Beautiful Soup
- Datetime

## Reference
API hosted on Replit (https://replit.com) with UptimeRobot (https://uptimerobot.com)
