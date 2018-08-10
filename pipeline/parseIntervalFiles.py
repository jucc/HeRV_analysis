# -*- coding: utf-8 -*-

"""
Parses RR files from the HeRV directory, where intervals are stored in files 
indexed by the hour of day. 
For example, all intervals from October 1st, from 14:00 to 14:59 would be 
stored in a file called rr17100114.csv.
"""

import csvUtils as csvu
from datetime import datetime, timedelta
from os import path


def get_filename(dt, dirname='.'):
    """
    returns the name of the file that contains intervals for a datetime
    Minutes and seconds are disregarded, the file represents the whole hour in the datetime
    If no file corresponding to this hour exists, will return None
    """
    filepattern = datetime.strftime(dt, '%y%m%d%H')
    regexp = r"^rr%s" % (filepattern)
    f = list(csvu.get_filenames(dirname = dirname, regexp=regexp))
    if len(f) > 0:
        return f[0]
    else:
        return None 


def get_intervals_from_file(filename):
    """
    lists all intervals (datetime and interval length) in a file
    """
    reader = csvu.get_rows(filename)
    rows = []
    for row in reader:        
        if len(row) > 1:
            rows.append({'date': csvu.time_from_string(row[0]), 
                         'interval':int(row[1])})
    return rows


def get_intervals_by_hour(dt, dirname="."):
    """
    lists all intervals in a given hour
    @param[in] dt - datetime with the hour queried. Minutes and seconds will be disregarded
    Example: 
    getIntervalsByHour(dt)
    will return all intervals recorded for 2017-10-01 from 14:00:00 to 14:59:59
    """
    filename = get_filename(dt, dirname)
    if filename:
        return get_intervals_from_file(filename)
    else:
        return []    
   
   
def get_day_intervals(user, dt, dirname="."):
    """
    lists all intervals in a given day (year, month day, from 00:00 to 23:59)
    """    
    beg = dt.replace(hour=0, minute=0, second = 0)
    end = dt.replace(hour=23, minute=59, second = 59)
    return get_intervals(user, beg, end, dirname)


def get_intervals(user, start_dt, end_dt, dirname="."):
    """
    lists all intervals recorded in the period of time between start_dt and end_dt
    @param[in]: start_dt and end_dt as datetimes
    """
    user_path = path.join(dirname, str(user))
    intervals = []
    for hour in csvu.fullhours(start_dt, end_dt):
        intervals.extend(get_intervals_by_hour(hour, user_path))
    return [x for x in intervals if x['date'] > start_dt and x['date'] < end_dt]


def count_intervals_by_day(user, dt_start, dt_end, dirname='.'):
    """
    returns a list of tuples containing the date and the number of intervals recorded
    for each day between the dates given (only contains days with at leats one interval recorded)
    """
    days = [get_intervals(user, dt, dt + timedelta(days=1), dirname) for dt in csvu.gendays(dt_start, dt_end)]
    return [(day[0]['date'], len(day)) for day in days if len(day) > 0]
