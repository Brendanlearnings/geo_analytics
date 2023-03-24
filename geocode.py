from opencage.geocoder import OpenCageGeocode
import json
import datetime 

# API key value 
key = "c4b6309106ef4859ae4c30d240067958"
geocoder = OpenCageGeocode(key)

def geocode(location):
    request = geocoder.geocode(location)

    json_dict = json.loads(request)

    geocoding_lat = geocoder.geocode(json_dict)['geometry']['lat']
    geocoding_long = geocoder.geocode(json_dict)['geometry']['lng']

    return [geocoding_lat,geocoding_long]