from opencage.geocoder import OpenCageGeocode
import datetime 

# API key value 
key = "5e28e026c47a478384384342fb05f229"
geocoder = OpenCageGeocode(key)

def geocode(location):
    geocoding_lat = geocoder.geocode(location[0], no_annotations="1")[0]['geometry']['lat']
    geocoding_long = geocoder.geocode(location[0], no_annotations="1")[0]['geometry']['lng']

    return [geocoding_lat,geocoding_long]