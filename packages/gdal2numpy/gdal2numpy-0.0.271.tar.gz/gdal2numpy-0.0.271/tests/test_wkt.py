import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = f"{workdir}/data/CLSA_LiDAR.tif"
fileshp = f"{workdir}/test_building.shp"

class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    def test_wkt(self):
        """
        test_read 
        """
        code = AutoIdentify(fileshp)
        print(code)


if __name__ == '__main__':
    unittest.main()



