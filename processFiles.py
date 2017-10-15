#!/bin/python
# -*- coding: utf-8 -*-

import os
import re
import csv


"""
lists all filenames in current directory matching the given regexp
"""
def getFilesMatching(regexp):
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
            rows.append({'date': row[0], 'interval':int(row[1])})
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
@input: year, month, day and hour as two-digit strings
Example: getIntervalsByHour('17', '10', '01', '14')
"""
def getIntervalsByHour(year, month, day, hour):    
    regexp = r"^rr%s%s%s%s" % (year, month, day, hour)
    match = getFilesMatching(regexp)
    if match:
        return getIntervalsFromFile(match[0])
    else:
        return None
    

RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HRV\\RawData\\0"
os.chdir(RAW_DATA_PATH)
print (getIntervalsByHour('17', '10', '01', '14'))
