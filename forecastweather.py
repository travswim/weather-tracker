import json
import urllib
from getidtz import city
from getidtz import findID
import time
import re
import sqlite3

lat1 = 49.364499
lon1 = -123.119300

url = 'http://api.openweathermap.org/data/2.5/forecast?id=6090786&mode=json&units=metric&APPID=77463ecfae956a3dd0d8c796115b8705'
jsonfile = 'forecast2.json'
jsonfile2 = 'weather2.py'

# Subclass of city for weather forcast parameters
class Weather(city):

    def __init__(self, ID, temp, hum, weatherID, main, desc, icon, clouds, wspeed, wdirec, date):
        self.ID = ID
        self.temp = temp
        self.hum = hum
        self.weatherID = weatherID
        self.main = main
        self.desc = desc
        self.icon = icon
        self.clouds = clouds
        self.wspeed = wspeed
        self.wdirec = wdirec
        self.date = date

    def getid(self):
        return self.ID

    def gettemp(self):
        return self.temp

    def gethum(self):
        return self.hum

    def getweatherID(self):
        return self.weatherID

    def getmain(self):
        return self.main

    def getdesc(self):
        return self.desc

    def geticon(self):
        return self.icon

    def getclouds(self):
        return self.clouds

    def getwspeed(self):
        return self.wspeed

    def getwdire(self):
        return self.wdirec

    def getdate(self):
        return self.date

# Conver wind direction from degrees
def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", \
    "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    #print arr[(val % 16)]
    return arr[(val % 16)]
    # Get Weather data from .json/url file

conn = sqlite3.connect('weatherdb.sqlite') #remove file if it already exists
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS City;
DROP TABLE IF EXISTS Weather;


CREATE TABLE City (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    c_id  INTEGER,
    city TEXT UNIQUE,
    country TEXT UNIQUE,
    lattitude REAL,
    longitude REAL,
    timezone TEXT UNIQUE
);

CREATE TABLE Weather (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    city_id  INTEGER,
    temp REAL,
    hum INTEGER,
    weatherID INTEGER,
    main TEXT UNIQUE,
    description TEXT UNIQUE,
    icon TEXT UNIQUE,
    clouds INTEGER,
    wspeed REAL,
    wdirec TEXT UNIQUE,
    dt TEXT UNIQUE

);
''')
get = findID(lat1, lon1)

# Read weather files and store data in class
def getWeather(filejs):
#def getWeather(url):
    try:
        x = (open(filejs)).read()
        #x = (urllib.urlopen(url)).read()
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
        dt = item['dt_txt']
        if re.match('\d+', str(js['cnt'])) == True:
            dt = datetime.now()
        else:
            pass
# This works but need to assing individual Id's. use id() function?

        identity = id(js['city']['id'])
        identity = Weather(js['city']['id'], temp, hum, weatherID, main, desc, \
        icon, clouds, wspeed, wdirec, dt)

        ID = get['ID']
        name = get['city']
        country = get['country']
        latt = get['lattitude']
        longit = get['longitude']
        tz = get['tz']

        cur.execute('''INSERT OR IGNORE INTO City (c_ID, city, country, lattitude, longitude, timezone)
            VALUES ( ?, ?, ?, ?, ?, ? )''', ( ID, name, country, latt, longit, tz ) )
        #cur.execute('SELECT id FROM City WHERE name = ? ', (ID, ))
        #city_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Weather (city_id, temp, hum, weatherID, main, description, icon, clouds, wspeed, wdirec, dt)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( ID, temp, hum, weatherID, main, desc, icon, clouds, wspeed, wdirec, dt ) )

        conn.commit()

    return {'temp':temp, 'hum':hum, 'id': weatherID, 'main':main, \
    'desc':desc, 'icon':icon, 'clouds':clouds, 'wspeed':wspeed, \
    'wdirec':wdirec, 'date':dt}

    js.close()

# Get weather icon url
def getWeatherIcon(icon):
    wurl = 'http://openweathermap.org/img/w/'
    end = '.png'
    wurl = wurl + icon + end
    return wurl

getWeather(jsonfile)
