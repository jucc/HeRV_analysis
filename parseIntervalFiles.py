# -*- coding: utf-8 -*-

"""
Parses RR files from the HeRV directory, where intervals are stored in files 
indexed by the hour of day. For example, all intervals from October 1st, 
from 14:00 to 14:59 would be stored in a file called rr17100114.csv.
"""

import csvUtils as csvu
from datetime import datetime, timedelta


"""
returns the name of the file that contains intervals for a datetime
Minutes and seconds are disregarded, the file represents the whole hour in the datetime
If no file corresponding to this hour exists, will return None
"""
def getFilename(dt, dirname='.'):
    filepattern = datetime.strftime(dt, '%y%m%d%H')
    regexp = r"^rr%s" % (filepattern)
    f = list(csvu.getFilenames(dirname = dirname, regexp=regexp))
    if len(f) > 0:
        return f[0]
    else:
        return None


"""
lists all intervals (datetime and interval length) in a file
"""
def getIntervalsFromFile(filename):
    reader = csvu.getFileReader(filename)
    rows = []
    for row in reader:        
        if len(row) > 1:
            rows.append({'date': csvu.timeFromString(row[0]), 
                         'interval':int(row[1])})
    return rows



"""
lists all intervals in a given hour
@param[in] dt - datetime with the hour queried. Minutes and seconds will be disregarded
Example: 
getIntervalsByHour(dt)
will return all intervals recorded for 2017-10-01 from 14:00:00 to 14:59:59
"""
def getIntervalsByHour(dt, dirname="."):
    filename = getFilename(dt, dirname)
    if filename:
        return getIntervalsFromFile(filename)
    else:
        return []
    
   
"""
lists all intervals (datetime and interval length) recorded in a period of time
between start_dt and end_dt
@param[in]: start_dt and end_dt as datetimes
"""
def getIntervals(start_dt, end_dt, dirname="."):
    
    intervals = getIntervalsByHour(start_dt, dirname)
    for i in range(int((end_dt-start_dt).seconds/3600)):
        intervals.extend(getIntervalsByHour(start_dt + timedelta(hours=i), dirname))
    return list(filter(lambda x: x['date'] > start_dt and x['date'] < end_dt, intervals))

    
if __name__ == '__main__':
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\RawData\\0"
    dt = datetime.strptime('2017-10-01 14:15:16', "%Y-%m-%d %H:%M:%S")
    mfilename=getFilename(dt, RAW_DATA_PATH)
    print(mfilename)
    print('#intervals: %d'%len(getIntervalsFromFile(mfilename)))
    print('#intervals in 1 hour : %d'%len(getIntervalsByHour(dt, RAW_DATA_PATH)))
    print('#intervals in 3 hours: %d'%len(getIntervals(dt, dt+timedelta(hours=3), RAW_DATA_PATH)))

    dt1 = datetime.strptime('2017-09-30 09:50:00', "%Y-%m-%d %H:%M:%S")
    dt2 = datetime.strptime('2017-09-30 10:0:00', "%Y-%m-%d %H:%M:%S")
    print('#intervals with bug: %d'%len(getIntervals(dt1, dt2, RAW_DATA_PATH)))