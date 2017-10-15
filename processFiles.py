#!/bin/python
# -*- coding: utf-8 -*-

import os
import re
import csv
from datetime import datetime, timedelta


"""
lists all filenames in current directory matching the given regexp
"""
def getFileMatching(regexp):
    return list(filter(lambda x: re.match(regexp, x), os.listdir()))


"""
lists all intervals (datetime and interval length) in a file
"""
def getIntervalsFromFile(filename):
    lines = list(filter(lambda x : len(x) > 3, open(filename, 'r').readlines()))
    reader = csv.reader(lines, delimiter=',')
    rows = []
    for row in reader:
        if len(row) > 1:
            rows.append({'date': datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), 'interval':int(row[1])})
    return rows


"""
lists the lengths of all intervals contained in a file
"""
def getRawIntervalsFromFile(filename):
    try:
        lines = list(filter(lambda x : len(x) > 3, open(filename).readlines()))
        return list(map(lambda x: int(x.split(',')[-1].strip()), lines))
    except:
        return None


"""
lists all intervals (datetime and interval length) recorded in a specific hour
@param[in]: dt - datetime with hour precision, will disregard minutes and seconds
Example: 
"""
def getIntervalsByHour(dt):
    filepattern = datetime.strftime(dt, '%y%m%d%H')
    regexp = r"^rr%s" % (filepattern)
    match = getFileMatching(regexp)
    if match:
        return getIntervalsFromFile(match[0])
    else:
        return None
    
    
"""
lists all intervals (datetime and interval length) recorded in a period of time
between start_dt and end_dt
@param[in]: start_dt and end_dt as datetimes
"""
def getIntervals(start_dt, end_dt):
    return []

    

RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HRV\\RawData\\0"
os.chdir(RAW_DATA_PATH)
td = '2017-10-01 14:15:16'
bi = datetime.strptime(td, "%Y-%m-%d %H:%M:%S")
print(bi.hour)
print (getIntervalsByHour(bi))
