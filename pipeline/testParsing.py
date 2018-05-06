# -*- coding: utf-8 -*-
"""
unit tests for parsing interval and activity files
"""

import numpy as np
import unittest
import csvUtils as csvu
import parseIntervalFiles as pif
import parseActivityFiles as paf


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.dt1 = csvu.timeFromString('2017-12-31 20:33:19')
        self.dt2 = csvu.timeFromString('2017-12-31 20:39:36')
        self.dt3 = csvu.timeFromString('2017-12-31 23:59:36')
        self.dt4 = csvu.timeFromString('2018-01-01 00:10:00')
        self.dt5 = csvu.timeFromString('2018-01-04 01:10:36')    

    def test_same_hour(self):
        f = [x for x in pif.fullhours(self.dt1, self.dt2)]        
        assert(len(f) == 1)

    def test_same_day(self):    
        f = [x for x in pif.fullhours(self.dt1, self.dt3)]        
        assert(len(f) == 4)

    def test_switch_day(self):
        f = [x for x in pif.fullhours(self.dt3, self.dt4)]        
        assert(len(f) == 2)

    def test_multiple_days(self):
        f = [x for x in pif.fullhours(self.dt1, self.dt5)]
        assert(len(f) == 78)


if __name__ == '__main__':
    unittest.main()