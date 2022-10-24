from flask import Flask
from flask_restful import Api, Resource
import urllib.request as ul
from bs4 import BeautifulSoup as soup

app = Flask(__name__)
api = Api(app)

class stationCode(Resource):
    def get(self, name):
        try:
            stationName = str(name)
        except:
            return {"error":"input error"}
        
        firstCharacter = stationName[0].upper()

        url = 'https://en.wikipedia.org/wiki/UK_railway_stations_%E2%80%93_' + firstCharacter
        req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        client = ul.urlopen(req)
        htmldata = client.read()
        client.close()

        pagesoup = soup(htmldata, "html.parser")
        itemlocator = pagesoup.findAll('table')
        stationLocator = itemlocator[1]

        stationList = stationLocator.findAll('tr')
        counter = 0
        for i in stationList:
            if counter == 0:
                counter = counter + 1
            else:
                info = i.findAll('a')
                name = info[0].text
                if name.lower().startswith(stationName.lower()):
                    return {"stationName": info[0].text, "code": info[2].text}
        return {"error": "station not found"}
        
class arrival(Resource):
    def get(self, code):
        try:
            stationCode = str(code)
        except:
            return {"error": "input error"}
        try:
            response = {}

            url = 'https://ojp.nationalrail.co.uk/service/ldbboard/dep/' + stationCode.upper()
            req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            client = ul.urlopen(req)
            htmldata = client.read()
            client.close()

            pagesoup = soup(htmldata, "html.parser")
            itemlocator = pagesoup.findAll('table')
            departureBoard = itemlocator[0]

            serviceLocator = departureBoard.tbody.findAll('tr')
            counter = 0
            for i in serviceLocator:
                infoLocator = i.findAll('td')
                time = infoLocator[0].text
                destination = infoLocator[1].text.replace("\n",'').lstrip()
                destination = " ".join(destination.split())
                status = infoLocator[2].text
                status = " ".join(status.split())
                platform = infoLocator[3].text
                response[counter] = {"time": time, "destination": destination, "status": status, "platform": platform}
                counter = counter + 1
            return response
        except:
            return {"error": "station not found"}

api.add_resource(stationCode, "/code/<string:name>")
api.add_resource(arrival, "/arrival/<string:code>")

if __name__ == "__main__":
    app.run()