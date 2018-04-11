# -*- coding: utf-8 -*-

"""
Parses RR files from the HeRV directory, where intervals are stored in files 
indexed by the hour of day. For example, all intervals from October 1st, 
from 14:00 to 14:59 would be stored in a file called rr17100114.csv.
"""

import csvUtils as csvu
from datetime import datetime, timedelta
from os import path


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
def get_intervals_by_hour(dt, dirname="."):
    filename = getFilename(dt, dirname)
    if filename:
        return getIntervalsFromFile(filename)
    else:
        return []
    
    
"""
counts how many whole hours are between two datetimes 
"""
def hourcount (start_dt, end_dt):
    td = end_dt-start_dt
    return int(td.days * 24 + td.seconds/3600)
   
    
"""
lists all intervals recorded in the period of time between start_dt and end_dt
@param[in]: start_dt and end_dt as datetimes
"""
def get_intervals(start_dt, end_dt, dirname="."):    
    intervals = []
    for i in range(hourcount(start_dt, end_dt)):
        intervals.extend(get_intervals_by_hour(start_dt + timedelta(hours=i), dirname))
    return [x for x in intervals if x['date'] > start_dt and x['date'] < end_dt]


"""
lists all intervals in a given day (year, month day, from 00:00 to 23:59)
"""
def get_day_intervals(year, month, day, dirname):
    date = str(year) + '-' + str(month) + '-' + str(day) + ' '
    stamp = "%Y-%m-%d %H:%M:%S"
    beg = datetime.strptime(date + '00:00:00', stamp)
    end = datetime.strptime(date + '23:59:00', stamp)

    return get_intervals(beg, end, dirname)


"""
aux function to iterate over days between two dates
"""
def iterate_dates(dt_start, dt_end):
    while dt_start <= dt_end:
        yield dt_start
        dt_start = dt_start + timedelta(days=1)
    return


"""
returns a list of tuples containing the date and the number of intervals recorded
for each day between the dates given (only contains days with at leats one interval recorded)
"""
def count_intervals_by_day(dt_start, dt_end, dirname='.'):
    days = [get_day_intervals(year=dt.year, month=dt.month, day=dt.day, dirname=dirname) 
                 for dt in iterate_dates(dt_start, dt_end)]
    return [(day[0]['date'], len(day)) for day in days if len(day) > 0]
                              
    
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