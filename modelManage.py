import pandas as pd
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metroBackend.settings")
import django
django.setup()

from MyApp.models import Station

DIR_PATH = 'MyApp/dataset/stations_node.csv'
def addStation():
    global DIR_PATH
    df = pd.read_csv(DIR_PATH)
    data = []

    for ele in range(len(df)):
        print(ele)
        dat = {
            'lat' : float(df['위도'][ele]),
            'lon' : float(df['경도'][ele]),
            'stationNum' : df['역번호'][ele],
            'stationName' : df['역이름'][ele],
            'lineNum' : df['호선'][ele],
            'transfer' : df['환승(없다면0)'][ele],
            'address' : df['주소'][ele]
        }
        data.append(dat)
    return data


Station.objects.all().delete()
data = addStation()
for d in data:
    s = Station(
        lineNumber=d['lineNum'],
        stationName=d['stationName'],
        stationNum=d['stationNum'],
        latitude=d['lat'],
        longitude=d['lon'],
        transfer=d['transfer'],
        address=d['address']
    )
    s.save()

print(Station.objects)