import requests
import tkinter as tk

loc = 21076
api = "1d67d07f578f4c48a4e92303222606"
r = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api}&q={loc}&aqi=no")
data = r.json()


class Data:
    """General API and location data"""
    def __init__(self, app):
        self.app = app
        self.loc = app.location
        self.api_key = app.api_key
        self.api_url = f"http://api.weatherapi.com/v1/forecast.json?key={api}&q={loc}&days=3&aqi=no&alerts=yes"
        #self.api_url = f"http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={self.loc}6&days=3&aqi=no&alerts=yes"
        self.req = requests.get(self.api_url)
        self.data = self.req.json()
        self.location = self.data['location']
        self.city = tk.StringVar(app.window, self.data['location']['name'])
        self.state = self.data['location']['region']
        self.country = self.data['location']['country']
        self.lat = self.data['location']['lat']
        self.lon = self.data['location']['lon']
        self.time_z = self.data['location']['tz_id']
        self.loc_time = tk.StringVar(app.window, self.data['location']['localtime'])
        self.current = self.data['current']


class WNow:
    """The current weather summary"""
    def __init__(self, main, app):
        self.data = app['current']
        self.temp_c = self.data['temp_c']
        self.temp_f = tk.StringVar(main.window, str(self.data['temp_f']) + '°F')
        self.condition = tk.StringVar(main.window, self.data['condition']['text'])
        self.icon_loc = self.data['condition']['icon']
        self.wind = self.data['wind_mph']
        self.wind_dir = self.data['wind_dir']
        self.precip = self.data['precip_in']
        self.humidity = self.data['humidity']
        self.real_feel = tk.StringVar(main.window, str(self.data['feelslike_f']) + '°F')
        self.vis_m = self.data['vis_miles']
        self.uv = self.data['uv']
        self.is_day = self.data['is_day']


class ForcastTday:
    """Overview of today's forcast"""
    def __init__(self, main, app):
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


class HourlyW:
    """Get the hourly weather data, max three days (day:0 = today, hr:10 = 10:00)"""
    def __init__(self, app, day=0, hr=0):
        self.h_data = app['forecast']['forecastday'][day]['hour'][hr]
        self.r_time = self.h_data['time']
        self.temp_f = self.h_data['temp_f']
        self.is_day = self.h_data['is_day']
        self.w_summary = self.h_data['condition']['text']
        self.w_icon = self.h_data['condition']['icon']
        self.wind_mph = self.h_data['wind_mph']
        self.precip_in = self.h_data['precip_in']
        self.humidity = self.h_data['humidity']
        self.feelslike_f = self.h_data['feelslike_f']
        self.heatindex_f = self.h_data['heatindex_f']
        self.chance_of_rain = self.h_data['chance_of_rain']
        self.chance_of_snow = self.h_data['chance_of_snow']
        self.vis_miles = self.h_data['vis_miles']
        self.gust_mph = self.h_data['gust_mph']
        self.uv = self.h_data['uv']


class WData:
    """Access to the main classes, call hourly data via \"HourlyW\""""
    def __init__(self, app):
        self.gen_data = Data(app)
        self.weather_now = WNow(app, self.gen_data.data)
        self.forcast_today = ForcastTday(app, self.gen_data.data)






