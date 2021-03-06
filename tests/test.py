import unittest
from ..main import get_rings_coords

class RequestTest(unittest.TestCase):

    def test_connection(self):
        URL = "http://www.aisgzk.kz/aisgzk/Proxy/aisgzkZem2/MapServer/identify?f=json&tolerance=1&returnGeometry=true&returnFieldName=false&returnUnformattedValues=false&imageDisplay=610%2C636%2C96&geometry=%7B%22x%22%3A7944865.56165178%2C%22y%22%3A6654452.032130188%7D&geometryType=esriGeometryPoint&sr=3857&mapExtent=7944635.84257453%2C6654209.782921452%2C7944954.316749808%2C6654541.831405841&layers=all%3A259"
        get_rings_coords(URL)
        self.
