from opencage.geocoder import OpenCageGeocode
import datetime 

# API key value 
key = "c4b6309106ef4859ae4c30d240067958"
geocoder = OpenCageGeocode(key)

def geocode(location):
    geocoding_lat = geocoder.geocode(location)['geometry']['lat']
    geocoding_long = geocoder.geocode(location)['geometry']['lng']

    return [geocoding_lat,geocoding_long]