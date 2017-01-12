import xml.etree.ElementTree as ET
import sqlite3

# import getidtz and forcastweather and link variables

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


fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict') # 3rd level dictionary
print 'Dict count:', len(all)
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Weather')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None :
        continue

    print name, artist, album, count, rating, length

    cur.execute('''INSERT OR IGNORE INTO City (ID, city, country, lattitude, longitude, timezone)
        VALUES ( ?, ?, ?, ?, ?, ? )''', ( ID, name, country, latt, longit, tz ) )
    cur.execute('SELECT id FROM City WHERE ID = ? ', (ID, ))
    city_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Weather (city_id, temp, hum, weatherID, main, description, icon, clouds, wspeed, wdirec, dt)
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( temp, hum, weatherID, main, description, icon, clouds, wspeed, wdirec, dt ) )

    conn.commit()
