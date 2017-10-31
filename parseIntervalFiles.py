#!/bin/python
# -*- coding: utf-8 -*-
"""
Parses RR files from the HeRV directory, where intervals are stored in files 
indexed by the hour of day. For example, all intervals from October 1st, 
from 14:00 to 14:59 would be stored in a file called rr17100114.csv.
"""
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
returns the name of the file that contains intervals for a datetime
Minutes and seconds are disregarded, the file represents the whole hour in the datetime
If no file corresponding to this hour exists, will return None
"""
def getFilename(dt):
    filepattern = datetime.strftime(dt, '%y%m%d%H')
    regexp = r"^rr%s" % (filepattern)
    match = getFileMatching(regexp)
    if match:
        return match[0]
    else:
        return None


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
lists all intervals in a given hour
@param[in] dt - datetime with the hour queried. Minutes and seconds will be disregarded
Example: 
dt = datetime.strptime('2017-10-01 14:15:16', "%Y-%m-%d %H:%M:%S")
getIntervalsByHour(dt)
will return all intervals recorded for 2017-10-01 from 14:00:00 to 14:59:59
"""
def getIntervalsByHour(dt):
    filename = getFilename(dt)
    if filename:
        return getIntervalsFromFile(filename)
    else:
        return []
    
   
"""
lists all intervals (datetime and interval length) recorded in a period of time
between start_dt and end_dt
@param[in]: start_dt and end_dt as datetimes
"""
def getIntervals(start_dt, end_dt):
    
    intervals =[]
    for i in range(int((end_dt-start_dt).seconds/3600)):
        intervals.extend(getIntervalsByHour(start_dt + timedelta(hours=i)))    
    return list(filter(lambda x: x['date'] > start_dt and x['date'] < end_dt, intervals))

    
if __name__ == '__main__':
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HRV\\RawData\\0"
    os.chdir(RAW_DATA_PATH)
    dt = datetime.strptime('2017-10-01 14:15:16', "%Y-%m-%d %H:%M:%S")
    print (len(getIntervalsByHour(dt)))
    print (len(getIntervals(dt, dt+timedelta(hours=2))))
