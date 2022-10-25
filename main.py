from flask import Flask
from flask_restful import Api, Resource
import urllib.request as ul
from bs4 import BeautifulSoup as soup
import datetime

app = Flask(__name__)
api = Api(app)

class stationCode(Resource):
    def get(self, name):
        try:
            stationName = str(name)
            if len(stationName) != 3:
                return {}, 400
        except:
            return {}, 400
        
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
        return {}, 404
        
class arrival(Resource):
    def get(self, code):
        try:
            stationCode = str(code)
            if len(stationCode) != 3:
                return {}, 400
        except:
            return {}, 400
        try:
            response = []

            url = 'https://ojp.nationalrail.co.uk/service/ldbboard/dep/' + stationCode.upper()
            req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            client = ul.urlopen(req)
            htmldata = client.read()
            client.close()

            pagesoup = soup(htmldata, "html.parser")
            itemlocator = pagesoup.findAll('table')
            departureBoard = itemlocator[0]

            serviceLocator = departureBoard.tbody.findAll('tr')
            for i in serviceLocator:
                infoLocator = i.findAll('td')
                time = infoLocator[0].text
                destination = infoLocator[1].text.replace("\n",'').lstrip()
                destination = " ".join(destination.split())
                status = infoLocator[2].text
                status = " ".join(status.split())
                platform = infoLocator[3].text
                response.append({"time": time, "destination": destination, "status": status, "platform": platform})
            return response
        except:
            return {}, 404

api.add_resource(stationCode, "/code/<string:name>")
api.add_resource(arrival, "/arrival/<string:code>")

if __name__ == "__main__":
    app.run()
