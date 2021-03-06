import requests
import csv
from pprint import pprint
import json
import geojson
import shapely.wkt
import csv


URL = "http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/"
ADDITIONAL_PARAMS = "&geometryType=esriGeometryPoint&sr=3857&mapExtent=7944789.369315789%2C6654446.452306012%2C7944809.273951744%2C6654467.205336286&layers=all%3A259"
HEADERS = {
    "Host": "www.aisgzk.kz",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "Referer": "http://www.aisgzk.kz/aisgzk/ru/content/maps/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

def make_point(point) -> str:
    """
    make url from point (X,Y) in 3857 srid
    """
    point = '{{"x":{},"y":{}}}'.format(point[0],point[1])
    return point

def get_rings_coords(url:str) -> list:
    """
    Request to aizk and by point coordinates and return polygon coords
    return: polygon coords
    TODO: add check for empty json
    """

    r = requests.get(url, headers = HEADERS)
    json_response = json.loads(r.text)["results"]
    if json_response:
        rings = json_response[0]["geometry"]["rings"][0]
        return rings
    else:
        return json_response

def get_points() -> list:
    """
    Read csv and get points
    return: list with list points [[x,y],[x1,x2] ...]
    """
    points = []
    with open('points.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        for row in reader:
            points.append(row[1:])
    return points

def get_extent(point: list) -> str:
    """
    Return points + 10 meter 
    return: map entend
    """
    x , y = point[0],point[1]
    result = "{},{},{},{}".format(str(float(x)-10),str(float(y)-10),str(float(x)+10),str(float(y)+10))
    return result

def get_wkt(rings:list) -> str:
    """
    Make wkt from polygon coordinates
    return: wkt Polygon 
    
    """
    coords = ""
    for ring in rings[:-1]:
        line = " ".join(map(str,ring)) + ","
        coords+=line
    coords+=" ".join(map(str,rings[-1]))
    pol_template = "POLYGON(({}))".format(coords)
    return pol_template

def make_geojson_from_wkt(wkt:str)-> str:
    """
    return: One geojson Feature
    TODO: add feature properties from kadastr
    """

    geometry = shapely.wkt.loads(wkt)
    feature = geojson.Feature(geometry = geometry ,properties={})
    return feature



def main():

    # url = URL + "identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry=%7B%22x%22%3A7944803.530974813%2C%22y%22%3A6654456.600407293%7D&geometryType=esriGeometryPoint&sr=3857&mapExtent=7932824.574822295%2C6641695.465075217%2C7953206.922039978%2C6662946.568075949&layers=all%3A259"
    # response = get_rings_coords(url) # can return empty list
    
    # wkt = get_wkt(response)
    # print(wkt)
    
    points = get_points()
    features = []
    for point in points:
        point_url = make_point(point)
        extent = get_extent(point)
        url = "http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry={geometry}&geometryType=esriGeometryPoint&sr=3857&mapExtent={extent}&layers=all%3A259" \
                .format(extent = extent, geometry = point_url )
        response = get_rings_coords(url)
        if response:
            wkt = get_wkt(response) 
            feature = make_geojson_from_wkt(wkt)
            features.append(feature)
        else:
            pass
    print(features)
    featrs_collection = geojson.FeatureCollection(features)
    dump = geojson.dumps(featrs_collection,sort_keys=True)
    with open("output.geojson","w") as file:
        file.write(dump)
    print(featrs_collection)

    #make Feature Collection and geojson file

#TODO add crs
#TODO do not read first line when reading csv

if __name__ == "__main__":
    main()