from opencage.geocoder import OpenCageGeocode
import json
import datetime 

# API key value 
key = "c4b6309106ef4859ae4c30d240067958"
geocoder = OpenCageGeocode(key)

#request = geocoder.geocode('2 Clam Road, Tableview, Cape Town')
#print(request)

def geocode(location):
    request = geocoder.geocode(location)
    request = request[0]
    
    lat = request['geometry']['lat']
    long = request['geometry']['lng']

    return [lat,long]
