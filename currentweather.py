import json
import urllib

# West Vancouver GPS coordinates
url = 'http://api.openweathermap.org/data/2.5/group?id=6090786&mode=json&units=metric&APPID=77463ecfae956a3dd0d8c796115b8705'
# Convert wind direction from angles to compass

class city(object):

    def _init_(self, id, name, country, lat, lon):
        self.id = id
        self.name = name
        self.country = country
        self.lat = lat
        self.lon = lon

    def getid(self):
        return self.id

    def getname(self):
        return self.name

    def getcountry(self):
        return self.country

    def getlat(self):
        return self.lat

    def getlon(self):
        return self.lon

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", \
    "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    #print arr[(val % 16)]
    return arr[(val % 16)]
    # Get Weather data from .json/url file
def getWeather(url):
#def getWeather(url):

    try:
        #x = (open('weathertest.json')).read()
        x = (urllib.urlopen(url)).read()
        #print "Read OK"
    except:
        print "Reading Failed"
    js = json.loads(x)
    lst = js['list']
    for item in lst:
        temp = item['main']['temp']
        hum = item['main']['humidity']
        weather = item['weather']
        for items in weather:
            weatherID = items['id']
            main = str(items['main'])
            desc = str(items['description'])
            icon = getWeatherIcon(str(items['icon']))
        clouds = item['clouds']['all']
        wspeed = item['wind']['speed']
        wdirec = degToCompass(item['wind']['deg'])
        #date = str(item['dt_txt'])

    return {'temp':temp, 'hum':hum, 'id': weatherID, 'main':main, \
    'desc':desc, 'icon':icon, 'clouds':clouds, 'wspeed':wspeed, \
    'wdirec':wdirec}

# Get weather icon url
def getWeatherIcon(icon):
    wurl = 'http://openweathermap.org/img/w/'
    end = '.png'
    wurl = wurl + icon + end
    return wurl

print getWeather(url)
