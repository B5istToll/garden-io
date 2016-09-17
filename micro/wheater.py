import os
import urllib.request
from flask import json

class Wheater:

    api_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=7287650&APPID=e678f345b0655798068aae42e86d3c77&cnt=10'

    @staticmethod
    def get_rain_prediction():

        rain_file_path = 'rain.json'
        # Try to read from the file first.
        if os.path.exists(rain_file_path):
            with open(rain_file_path) as f:
                rain = json.load(f)
        else:

            with urllib.request.urlopen(Wheater.api_url) as response:
                content = response.read()

            data = json.loads(content)
            rain = list(map(lambda x: x['rain'] if 'rain' in x else 0, data['list']))

            # Write to file for later use.
            with open(rain_file_path, 'w') as f:
                json.dump(rain, f)

        return rain
