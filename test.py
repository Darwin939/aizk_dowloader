import unittest
import requests
from main import get_rings_coords

class RequestTest(unittest.TestCase):

    def test_connection(self):
        URL = "http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/"
        response = requests.get(URL)
        self.assertEqual(response.status_code, 200, "Should return 200, check your internet connection. Returned status code is {}".format(str(response.status_code)) )
        
    def test_data_response(self):
        
        url = 'http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry=%7B%22x%22%3A7944845.722276927%2C%22y%22%3A6654452.554219%7D&geometryType=esriGeometryPoint&sr=3857&mapExtent=7944635.84257453%2C6654209.782921452%2C7944954.316749808%2C6654541.831405841&layers=all%3A259'
        response = get_rings_coords(url)
        self.assertListEqual(response,[],"Should return ")

if __name__ == '__main__':
    unittest.main()

