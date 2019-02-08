import unittest
from featurization.link_features import *

class LinkFeaturesTests(unittest.TestCase):

    def test_pmi(self):
        a = [3,4,5]
        b = [1,6,2]
        c = []
        W = 10
        self.assertAlmostEqual(npmi(a,b,W), -1)
        self.assertAlmostEqual(npmi(a,a,W), 1)
        self.assertAlmostEqual(npmi(a,c,W), -1)
        self.assertAlmostEqual(npmi(c, c, W), -1)

    def test_ngd(self):
        a = [3, 4, 5]
        b = [1, 6, 2]
        c = []
        W = 10
        self.assertAlmostEqual(ngd(a, b, W), NGD_DEFAULT)
        self.assertAlmostEqual(ngd(a, a, W), 0)
        self.assertAlmostEqual(ngd(a, c, W), NGD_DEFAULT)
        self.assertAlmostEqual(ngd(c,c,W), NGD_DEFAULT)

    def test_jaccard(self):
        a = [3, 4, 5]
        b = [1, 6, 2]
        c = []
        self.assertAlmostEqual(js(a, b), 0)
        self.assertAlmostEqual(js(a, a), 1)
        self.assertAlmostEqual(js(c, c), 0)

if __name__ == "__main__":

    # run unit tests
    unittest.main()