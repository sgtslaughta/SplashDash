import requests

loc = 21076
api = "1d67d07f578f4c48a4e92303222606"
r = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api}&q={loc}&aqi=no")
data = r.json()


class Data:
    def __init__(self, app):
        self.loc = app.location
        self.api_key = app.api_key
        self.req = requests.get(f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={self.loc}&aqi=no")
        self.data = self.req.json()
        self.location = data['location']
        self.city = data['location']['name']
        self.state = data['location']['region']
        self.country = data['location']['country']
        self.lat = data['location']['lat']
        self.lon = data['location']['lon']
        self.time_z = data['location']['tz_id']
        self.loc_time = data['location']['localtime']
        self.current = data['current']
        self.temp_c = data['current']['temp_c']
        self.temp_f = data['current']['temp_f']
        self.condition = data['current']['condition']['text']
        self.icon_loc = data['current']['condition']['icon']
        self.wind = data['current']['wind_mph']
        self.wind_dir = data['current']['wind_dir']
        self.precip = data['current']['precip_in']
        self.humidity = data['current']['humidity']
        self.real_feel = data['current']['feelslike_f']
        self.vis_m = data['current']['vis_miles']
        self.uv = data['current']['uv']
