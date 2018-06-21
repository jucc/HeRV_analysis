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
iterate over every full hour between two datetimes 
"""
def fullhours(start_dt, end_dt):
    start = start_dt.replace(minute=0, second=0)
    while start < end_dt:
        yield start
        start = start + timedelta(hours=1)   


"""
iterate over every day between two datetimes 
"""
def gendays(start_dt, end_dt):
    start = start_dt.replace(hour=0, minute=0, second=0)
    while start < end_dt:
        yield start
        start = start + timedelta(days=1)
    
"""
lists all intervals recorded in the period of time between start_dt and end_dt
@param[in]: start_dt and end_dt as datetimes
"""
def get_intervals(start_dt, end_dt, dirname="."):    
    intervals = []
    for hour in fullhours(start_dt, end_dt):
        intervals.extend(get_intervals_by_hour(hour, dirname))
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
