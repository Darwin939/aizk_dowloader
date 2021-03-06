import requests
import csv
from pprint import pprint
import json

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

def make_url() -> str:
    """
    make url from point (X,Y) in 3857 srid
    """
    pass

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
        print(json_response)


def get_wkt(rings:list) -> str:
    """
    Make wkt from polygon coordinates
    return: wkt Polygon 
    
    """
    coords = ""
    for ring in rings:
        line = " ".join(map(str,ring)) + ","
        coords+=line
    pol_template = "POLYGON(({}))".format(coords)
    return pol_template


def main():
    # url = URL + "identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry=%7B%22x%22%3A7944803.530974813%2C%22y%22%3A6654456.600407293%7D&geometryType=esriGeometryPoint&sr=3857&mapExtent=7944789.369315789%2C6654446.452306012%2C7944809.273951744%2C6654467.205336286&layers=all%3A259"
    url = "http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry=%7B%22x%22%3A7944865.56165178%2C%22y%22%3A6654452.032130188%7D&geometryType=esriGeometryPoint&sr=3857&mapExtent=7944635.84257453%2C6654209.782921452%2C7944954.316749808%2C6654541.831405841&layers=all%3A259"

    r = get_rings_coords(url)
    wkt = get_wkt(r)
    print(wkt)



if __name__ == "__main__":
    main()