from opencage.geocoder import OpenCageGeocode
import pandas as pd 

# API key value 
key = "c4b6309106ef4859ae4c30d240067958"
geocoder = OpenCageGeocode(key)


def geocode(location):

    request = geocoder.geocode(location)[0]
    
    df = pd.DataFrame(request)

    return df
