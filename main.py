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

class history(Resource):
    def get(self, departure, arrival, d):
        try:
            departureStation = str(departure)
            arrivalStation = str(arrival)
            date = str(d).replace('-','%2F')
        except:
            return {}, 400

        response = []
        try:
            url = 'https://www.recenttraintimes.co.uk/Home/Search?Op=Srch&Fr=' + departureStation + '&To=' + arrivalStation +'&TimTyp=D&TimDay=A&Days=Al&TimPer=Cu&dtFr=' + date + '&dtTo=' + date + '&ShwTim=AvAr&MxArCl=5&TOC=All&ArrSta=5&MetAvg=Mea&MetSpr=RT&MxScDu=&MxSvAg=&MnScCt='
            req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            client = ul.urlopen(req)
            htmldata = client.read()
            client.close()

            pagesoup = soup(htmldata, "html.parser")
            itemlocator = pagesoup.findAll('table')

            timetable = itemlocator[1]
            trainlocator = timetable.findAll('tr')

            counter = 0
            for train in trainlocator:
                if counter < 2:
                    counter = counter + 1
                else: 
                    if counter == 2:
                        counter = 0
                    trainInfo = train.findAll('td')
                    operator = trainInfo[0].text
                    scheduledDeparture = trainInfo[1].text
                    scheduledArrival = trainInfo[2].text
                    duration = trainInfo[3].text
                    realArrival = trainInfo[5].text.split()[0]

                    try:
                        startTime = datetime.datetime.strptime(scheduledArrival.split(':')[0] + ":" + scheduledArrival.split(':')[1] + ":00", "%H:%M:%S")
                    except:
                        startTime = datetime.datetime.strptime(scheduledArrival.replace('*','').split(':')[0] + ":" + scheduledArrival.replace('*','').split(':')[1] + ":00", "%H:%M:%S")
                    endTime = datetime.datetime.strptime(realArrival.split(':')[0] + ":" + realArrival.split(':')[1] + ":00", "%H:%M:%S")
                    diffTime = endTime - startTime
                    min = int(diffTime.total_seconds() / 60)
                    if min == 0:
                        late = 0
                    if min < 0:
                        midTime = datetime.datetime.strptime("00:00:00","%H:%M:%S")
                        timeChange = datetime.timedelta(minutes=1440)
                        diffTime = (endTime - midTime) + (midTime - startTime + timeChange)
                        min = int(diffTime.total_seconds() / 60)
                        late = min
                    else:
                        late = min

                    response.append({
                        "operator": operator,
                        "departureStation": departureStation.replace('+', ' '),
                        "arrivalStation": arrivalStation.replace('+', ' '),
                        "scheduledDeparture": scheduledDeparture,
                        "scheduledArrival": scheduledArrival,
                        "duration": duration,
                        "actualArrival": realArrival,
                        "late": late
                    })
            return response
        except:
            return {}, 404

api.add_resource(stationCode, "/code/<string:name>")
api.add_resource(arrival, "/arrival/<string:code>")
api.add_resource(history, "/history/<string:departure>/<string:arrival>/<string:d>")

if __name__ == "__main__":
    app.run()
