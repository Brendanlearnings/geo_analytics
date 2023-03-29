import requests
import json

def geocode(location):
    url = "https://atlas.microsoft.com/search/address/json"

    querystring = {"subscription-key":"gOpOAK_LpXt8qCWYwUwp9JRrscQ-xnrnpCtexOqaGS4","api-version":"1.0","language":"en-US","query":f"{location}"}

    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring).json()

    
    return response
