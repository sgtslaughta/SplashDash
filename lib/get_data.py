import requests
from datetime import datetime

loc = 21076
api = "1d67d07f578f4c48a4e92303222606"
r = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api}&q={loc}&aqi=no")
data = r.json()


class Data:
    def __init__(self, app):
        self.app = app
        self.loc = app.location
        self.api_key = app.api_key
        self.api_url = f"http://api.weatherapi.com/v1/forecast.json?key={api}&q={loc}&days=3&aqi=no&alerts=yes"
        #self.api_url = f"http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={self.loc}6&days=3&aqi=no&alerts=yes"
        self.req = requests.get(self.api_url)
        self.data = self.req.json()
        self.location = self.data['location']
        self.city = self.data['location']['name']
        self.state = self.data['location']['region']
        self.country = self.data['location']['country']
        self.lat = self.data['location']['lat']
        self.lon = self.data['location']['lon']
        self.time_z = self.data['location']['tz_id']
        self.loc_time = self.data['location']['localtime']
        self.current = self.data['current']


class WNow:
    def __init__(self, app):
        self.data = app['current']
        self.temp_c = self.data['temp_c']
        self.temp_f = self.data['temp_f']
        self.condition = self.data['condition']['text']
        self.icon_loc = self.data['condition']['icon']
        self.wind = self.data['wind_mph']
        self.wind_dir = self.data['wind_dir']
        self.precip = self.data['precip_in']
        self.humidity = self.data['humidity']
        self.real_feel = self.data['feelslike_f']
        self.vis_m = self.data['vis_miles']
        self.uv = self.data['uv']


class ForcastTday:
    def __init__(self, app):
        self.data = app['forecast']['forecastday'][0]
        self.astro = self.data['astro']
        self.day_stats = self.data['day']
        self.maxtemp_f = self.day_stats['maxtemp_f']
        self.mintemp_f = self.day_stats['mintemp_f']
        self.maxwind_mph = self.day_stats['maxwind_mph']
        self.totalprecip_in = self.day_stats['totalprecip_in']
        self.avgvis_miles = self.day_stats['avgvis_miles']
        self.avghumidity = self.day_stats['avghumidity']
        self.sunrise = self.astro['sunrise']
        self.sunset = self.astro['sunset']
        self.moonrise = self.astro['moonrise']
        self.moonset = self.astro['moonset']
        self.moon_phase = self.astro['moon_phase']

        print(self.data['hour'][0])


class WData:
    def __init__(self, app):
        self.gen_data = Data(app)
        self.weather_now = WNow(self.gen_data.data)
        self.forcast_today = ForcastTday(self.gen_data.data)





