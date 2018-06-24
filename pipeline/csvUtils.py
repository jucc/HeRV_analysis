# -*- coding: utf-8 -*-

"""
Parses csv files and delivers them as iterators of rows , with each row being 
a list of values.
Methods returning iterators can be converted to lists by calling list(method())
"""

import os
import re
import csv
from datetime import datetime

"""
lists all filenames in a directory that match a given regexp
"""
def get_filenames(dirname=".", regexp= r".*\.csv"):
    match_files = filter(lambda x: re.match(regexp, x), os.listdir(path=dirname))
    return [os.path.join(dirname, x) for x in match_files]


"""
lists all non-empty rows in a csv file. Each row is a list of columns
"""
def get_rows(filename):
    reader = csv.reader(open(filename, 'r').readlines(), delimiter=',')
    return [line for line in reader if any(line)]


def string_from_time_kubios(timestr):
    return datetime.strftime(timestr, "%Y-%m-%d %H:%M:%S.%f")[:-3]


def string_from_time_filename(timestr):
    return datetime.strftime(timestr, "%y-%m-%d-%H-%M")


def time_from_string(timestr):
    patterns = ["%Y-%m-%d %H:%M:%S", "%m/%d/%y %H:%M"]
    for pattern in patterns:
        try:
            return datetime.strptime(timestr, pattern)
        except:
            pass
    
    
def duration(start, stop):
    return  int((stop-start).seconds)


def printhours(datelist):
    for i in datelist:
        print (i.hour, end=', ')