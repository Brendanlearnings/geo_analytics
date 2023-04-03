import requests
import json


def route_matrix(points:list = [], avoid:list = [], departAt:str = None, compute_best_order:str = 'true', computeTravelTimeFor:str = 'all', RouteRepresentationForBestOrder:str = 'polyline', RouteType:str = 'fastest', travelMode:str = 'car', traffic:str = 'true') -> None:
    '''Using the azure maps route endpoints we are able to return a json object containing the route set for the given parameters'''
    # Setup the required parameters for the api query.
    url = 'https://atlas.microsoft.com/route/directions/json' 
    flattened_coords = ':'.join([','.join(map(str, coord)) for coord in points])
    aviods_poi = '&avoid='.join(poi for poi in avoid)
    if departAt == None:
        depart_at = ''
    else:
        depart_at = departAt 
        depart_at = f'{depart_at}'

    # Construct the Rest API request
    querystring = {'api-version':'1.0',"subscription-key":"gOpOAK_LpXt8qCWYwUwp9JRrscQ-xnrnpCtexOqaGS4",'query':f'{flattened_coords}','avoid':f'{aviods_poi}','departAt':f'{depart_at}','computeBestOrder':f'{compute_best_order}','computeTravelTimeFor':f'{computeTravelTimeFor}','routeRepresentation':f'{RouteRepresentationForBestOrder}','routeType':f'{RouteType}','travelMode':f'{travelMode}','traffic':f'{traffic}'}

    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring).json()

    return response



   
