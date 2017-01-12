n = 0
def FirstLine():
    f2.write('{\n  "places":[\n    {\n      ')
    return None
with open('city_list.json', 'r') as f1:
    with open('new_city_list.json', 'a') as f2:
        for line in f1:
            line = line.rstrip()    # strip the right side
            #line = line.split(',')     # split up the words
            #i = line[0].split('{')
            line = line.split('"')
            ID = '"' + line[1] + '"' +line[2]
            city = '"' + line[3] + '"' + line[4] + '"' + line[5] + '"'
            country = '"' + line[7] + '"' + line[8] + '"' + line[9] + '"'
            gps = '"' + line[11] + '":'
            lon =  '"' + line[13] + '"' + line[14]
            l = line[16].split('}')
            lat = '"' + line[15] + '"' + l[0]

            if n == 0:
                FirstLine()
                f2.write(ID +'\n      ')
                f2.write(city +',\n      ')
                f2.write(country+',\n      ')
                f2.write(gps + '{\n        ')
                f2.write(lon + '\n        ')
                f2.write(lat + '\n      }\n')
                f2.write('    },\n    {\n')
            elif n == 209578:
                f2.write('      ' + ID +'\n      ')
                f2.write(city +',\n      ')
                f2.write(country+',\n      ')
                f2.write(gps + '{\n        ')
                f2.write(lon + '\n        ')
                f2.write(lat + '\n      }\n')
                f2.write('    }\n  ]\n}')
            elif n > 0 or n <209578:
                f2.write('      ' + ID +'\n      ')
                f2.write(city +',\n      ')
                f2.write(country+',\n      ')
                f2.write(gps + '{\n        ')
                f2.write(lon + '\n        ')
                f2.write(lat + '\n      }\n')
                f2.write('    },\n    {\n')
            n += 1
