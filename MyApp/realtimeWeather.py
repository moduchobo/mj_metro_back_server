
'''
openweathermap.org
api_key = f54b13c3c6ecf6d1d51c6be402b095dc

https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
'''

import requests

APP_ID = "f54b13c3c6ecf6d1d51c6be402b095dc"

# response = requests.get('https://google.com')
# print(response)


def getWeatherData(lat, lon):
    global APP_ID
    print(APP_ID)
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APP_ID}')
    print(response.json())
    return response.json()


# for test...
# getWeatherData(37.22349686935068, 127.18721018723127)