import unittest
import requests
from main import get_rings_coords, get_wkt, make_url


class RequestTest(unittest.TestCase):

    def test_connection(self):
        """
        Test internet connection and test if you ip was blocked
        """
        URL = "http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/"
        response = requests.get(URL)
        self.assertEqual(response.status_code, 200, "Should return 200, check your internet connection. Returned status code is {}".format(str(response.status_code)) )
        
    def test_data_response(self):
        """
        Makes a request for an empty zone and checks 
        for the existence of an empty list
        """
        url = 'http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry=%7B%22x%22%3A7944845.722276927%2C%22y%22%3A6654452.554219%7D&geometryType=esriGeometryPoint&sr=3857&mapExtent=7944635.84257453%2C6654209.782921452%2C7944954.316749808%2C6654541.831405841&layers=all%3A259'
        response = get_rings_coords(url)
        self.assertListEqual(response,[],"Should return empty list")

class ResponseTest(unittest.TestCase):

    def test_wkt(self):
        """
        Test get_wkt function with 
        """
        polygon_example = [[7941214.280214552,6657013.482674685],[7941285.222167995,6657275.094877264],
                [7941646.696438557,6657174.27908272],[7941576.155582538,6656914.224977171],
                [7941214.280214552,6657013.482674685]]
        wkt = get_wkt(polygon_example)
        polygon_wkt =  "POLYGON((7941214.280214552 6657013.482674685,7941285.222167995 6657275.094877264,7941646.696438557 6657174.27908272,7941576.155582538 6656914.224977171,7941214.280214552 6657013.482674685,))"       
        self.assertEqual(wkt,polygon_wkt,"Should equal")


if __name__ == '__main__':
    unittest.main()

