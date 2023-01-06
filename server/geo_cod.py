import requests
import re
class GeoCod(object):
    def __init__(self,start_lon, start_lat, end_lon, end_lat):
        self.start_lon = start_lon
        self.start_lat =start_lat
        self.end_lon= end_lon
        self.end_lat= end_lat
    def geo_cod(self):
        self.body = {"coordinates": [[self.start_lon, self.start_lat], [self.end_lon, self.end_lat]]}
        self.headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
            'Content-Type': 'application/json; charset=utf-8'}
        self.call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=self.body,
                                  headers=self.headers)

        self.string_res = self.call.text



        self.tag = 'rtept'
        self.reg_str = '</' + self.tag + '>(.*?)' + '>'
        self.res = re.findall(self.reg_str, self.string_res)

        self.string1 = str(self.res)
        self.tag1 = '"'
        self.reg_str1 = '"' + '(.*?)' + '"'
        self.res1 = re.findall(self.reg_str1, self.string1)
        self.cod = {'cod': self.res1}
        return self.cod