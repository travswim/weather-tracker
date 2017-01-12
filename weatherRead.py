import json
#import urllib
jfile = 'weathertest.json'
def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    #print arr[(val % 16)]
    return arr[(val % 16)]
def getWeather(jsonFile):
#def getWeather(url):
    try:
        x = (open('weathertest.json')).read()
        #x = (urllib.urlopen(url)).read()
        #print "Read OK"
    except:
        print "Reading Failed"
    js = json.loads(x)
    lst = js['city']['list']
    for item in lst:
        temp = item['main']['temp']
        hum = item['main']['humidity']
        weather = item['weather']
        for items in weather:
            weatherID = items['id']
            main = str(items['main'])
            desc = str(items['description'])
            icon = str(items['icon'])
        clouds = item['clouds']['all']
        wspeed = item['wind']['speed']
        wdirec = degToCompass(item['wind']['deg'])
        date = str(item['dt_txt'])
    return {'temp':temp, 'hum':hum, 'id': weatherID, 'main':main, \
    'desc':desc, 'icon':icon, 'clouds':clouds, 'wspeed':wspeed, \
    'wdirec':wdirec, 'date':date}

print getWeather(jfile)
# lst = js['city']['list']
# for item in lst:
#     temp = item['main']['temp']
#     hum = item['main']['humidity']
#     weather = item['weather']
#     for items in weather:
#         weatherID = items['id']
#         main = items['main']
#         desc = items['description']
#         icon = items['icon']
#     clouds = item['clouds']['all']
#     wspeed = item['wind']['speed']
#     wdirec = degToCompass(item['wind']['deg'])
#     date = item['dt_txt']
#     print temp
#     print hum
#     print weatherID
#     print main
#     print desc
#     print icon
#     print clouds
#     print wspeed
#     print wdirec
#     print date
