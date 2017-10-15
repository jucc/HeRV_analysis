#!/bin/python
# -*- coding: utf-8 -*-

import os
import re


def getFilesMatching(regexp):
    return list(filter(lambda x: re.match(regexp, x), os.listdir()))


def getBeatsFromFile(filename):
    try:
        lines = filter(lambda x : len(x) > 3, open(filename).readlines())
        return list(map(lambda x: int(x.split(',')[-1].strip()), lines))
    except:
        return None


def getBeatsByHour(year, month, day, hour):    
    regexp = r"^rr%s%s%s%s" % (year, month, day, hour)
    match = getFilesMatching(regexp)
    if match:
        return getBeatsFromFile(match[0])
    else:
        return None


RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HRV\\RawData\\0"
os.chdir(RAW_DATA_PATH)
print (getBeatsByHour('17', '10', '01', '15'))