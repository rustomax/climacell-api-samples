# Demo script for ClimaCell API v2.

import requests
import random
import string
import os

API_BASE_URL = 'https://api2.climacell.co/v2/'

API_TOKEN = ""
if "CC_API_KEY" in os.environ:
    API_TOKEN = os.environ['CC_API_KEY']
else:
    quit()

headers = {'apikey': API_TOKEN}


print('Create a location using locations endpoint:')
# Randomizing location name, because it needs to be unique
location_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
data = {
    "name": location_name,
    "point": {"lon": -72.176, "lat": 41.303}
}
r = requests.post(API_BASE_URL + 'locations', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())
location_id = r.json()['id']


print('\nHistorical endpoint:')
data = {
    "geocode": {"lon": -72.176, "lat": 41.303},
    "start_time": "2018-07-01T12:00:00Z",
    "end_time": "2018-07-01T18:00:00Z",
    "timestep": 60,
    "fields": [{"name": "temp", "units": "F"}]
}
r = requests.post(API_BASE_URL + 'historical', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())


print('\nYou can use location_id for the predefined location, instead of geocode:')
data = {
    "location_id": location_id,
    "start_time": "2018-07-01T12:00:00Z",
    "end_time": "2018-07-01T18:00:00Z",
    "timestep": 60,
    "fields": [{"name": "temp", "units": "F"}]
}
r = requests.post(API_BASE_URL + 'historical', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())


print('\nRealtime endpoint - no "fields" means ALL weather parameters are returned:')
data = {
    "geocode": {"lon": -72.176, "lat": 41.303}
}
r = requests.post(API_BASE_URL + 'realtime', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())


print('\nNowcast endpoint:')
data = {
    "geocode": {"lon": -72.176, "lat": 41.303},
    "fields": [{"name": "feels_like", "units": "F"}]
}
r = requests.post(API_BASE_URL + 'nowcast', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())


print('\nHourly endpoint:')
r = requests.get(API_BASE_URL + 'weather/forecast/hourly/?lat=-72.176&lon=41.303&num_hours=5', headers=headers)
print("Status code:", r.status_code)
print(r.json())


print('\nDaily endpoint:')
r = requests.get(API_BASE_URL + 'weather/forecast/daily/?lat=-72.176&lon=41.303&num_days=3', headers=headers)
print("Status code:", r.status_code)
print(r.json())


print('\nWeather_map_layer endpoint:')
r = requests.get(API_BASE_URL + 'weather_map_layer/now/5/9/11.png', headers=headers)
print("Status code:", r.status_code)
print('Returned PNG tile, with file size:', len(r.text))


print('\nWeather_map_layer for a specific time:')
r = requests.get(API_BASE_URL + 'weather_map_layer/1541030400/5/9/11.png', headers=headers)
print("Status code:", r.status_code)
print('Returned PNG tile, with file size:', len(r.text))


print('\nCreate group using groups endpoint:')
group_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
data = {
    "name": group_name
}
r = requests.post(API_BASE_URL + 'groups', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())
group_id = r.json()['id']
group_name = r.json()['name']


print('\nAdd group member using members endpoint:')
data = {
    "first_name": "John", "last_name": "Smith", "email": "john@smoth.com", "phone": "123-456-7890"
}
r = requests.post(API_BASE_URL + 'groups' + group_id + "/members/", headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())


print('\nCreate Temperature alert using alerts endpoint:')
name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
data = {
    "name": "Temperature alert",
    "location_id": location_id,
    "notice": 60,
    "conditions": [{"parameter": "Temperature", "value": 0, "operator": "gt"}],
    "groups": [{"name": group_name, "delivery": { "sms": True, "email": True}}]
}
r = requests.post(API_BASE_URL + 'alerts', headers=headers, json=data)
print("Status code:", r.status_code)
print(r.json())
