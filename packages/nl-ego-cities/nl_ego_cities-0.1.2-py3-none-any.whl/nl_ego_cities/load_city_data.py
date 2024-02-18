import json
import pandas as pd
import numpy as np

from .city_coords import city_json
def location_json(city='', street=''):
    lat, lon = [None, None]
    if city != '':
        if city in city_json.keys():
            lat, lon = city_json[city]['lat'], city_json[city]['lon']
        else:
            lat = 91
            lon = 181
    return lat, lon
def get_location(city):
    lat, lon = location_json(city=city)
    return lat, lon
def get_lat_lon(df, city_column):
    """This function is get lat and long of the city column's value"""
    df['lat'], df['lon'] = zip(*df[city_column].apply(get_location))
    return df['lat'].values, df['lon'].values