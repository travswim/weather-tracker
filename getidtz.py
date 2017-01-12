import json
import urllib
import math

# West Vancouver GPS coordinates
lat1 = 49.364499
lon1 = -123.119300

class city(object):

    def __init__(self, ID, name, country, lat, lon, tz):
        self.ID = ID
        self.name = name
        self.country = country
        self.lat = lat
        self.lon = lon

    def getID(self):
        return self.ID

    def getname(self):
        return self.name

    def getcountry(self):
        return self.country

    def getlat(self):
        return self.lat

    def getlon(self):
        return self.lon

    def gettz(self):
        return self.tz

# Match GPS coordinates with city ID and city name and get .json url
def findID(Lattitude, Longitude):
    distance = None
    r = 6371 # Earth radius
    urlF = 'http://api.openweathermap.org/data/2.5/forecast?id='
    urlC = 'http://api.openweathermap.org/data/2.5/group?id='
    owapiKey = '&APPID=77463ecfae956a3dd0d8c796115b8705'
    metric = '&units=metric'
    imperial = '&units=imperial'
    lang = '&lang=en'
    mode = '&mode=json'
    try:
        x = (open('new_city_list.json')).read()
    except:
        print "Reading Failed"
    try:
        js = json.loads(x)
    except:
        print "Decoding FAILED"

    for item in js['places']:
        # Great Circle Equation betwen coordinates:
        # d = r * acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1-lon2))
        try:
            lat = item['coord']['lat']
            lon = item['coord']['lon']
            d = r*math.acos(math.sin(math.radians(Lattitude)) * \
            math.sin(math.radians(lat)) + math.cos(math.radians(Lattitude)) \
            * math.cos(math.radians(lat)) * \
            math.cos(math.radians(Longitude-lon)))

            if distance == None or distance > d:
                distance = d
                ID = item["_id"]
                name = item["name"]
                country = item["country"]
                latt = item['coord']['lat']
                longit = item['coord']['lon']
                tz = str(getTimezone(Lattitude, Longitude))
            else: continue
        except:
            print "Error"
    if country == 'US':
        urlForcast = urlF + str(ID) + mode + imperial + owapiKey
        urlCurrent = urlC + str(ID) + mode + imperial + owapiKey
    else:
        urlForcast = urlF + str(ID) + mode + metric + owapiKey
        urlCurrent = urlC + str(ID) + mode + metric + owapiKey
    place = city(ID, str(name), str(country), lat, lon, tz)
    print place.getcountry()
    #return None
    return {"forcast":urlForcast, "current": urlCurrent, "ID":ID, "city":name,\
    "country":country, "lattitude":latt, "longitude":longit, \
    "tz":getTimezone(Lattitude, Longitude)}

# Get time zone of GPS coordinates
def getTimezone(Lattitude, Longitude):
    gapiKey = 'AIzaSyCe2vjSsiD5wc1TmbdmYI0T-K7e21ecRNI'
    url ='https://maps.googleapis.com/maps/api/timezone/json?location=' \
    + str(Lattitude) + ',' + str(Longitude) + '&timestamp=1458000000&key=' \
    + gapiKey
    x = (urllib.urlopen(url)).read()
    js = json.loads(x)
    tz = js['timeZoneName']
    return tz


#print findID(lat1, lon1)
