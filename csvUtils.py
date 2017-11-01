# -*- coding: utf-8 -*-

"""
Parses csv files and delivers them as iterators of rows , with each row being 
a list of values.
Methods returning iterators can be converted to lists by calling list(method())
"""

import os
import re
import csv


"""
Iterator yielding all filenames in a directory that match a given regexp
"""
def getFilenames(dirname=".", regexp= r".*\.csv"):
    match_files = filter(lambda x: re.match(regexp, x), os.listdir(path=dirname))
    return [os.path.join(dirname, x) for x in match_files]


"""
Iterator yielding all non-empty rows in a csv file.
Each row is a list of columns
"""
def getFileReader(filename):
    reader = csv.reader(open(filename, 'r').readlines(), delimiter=',')
    return filter(lambda x : len(x) > 1, reader)


"""
Iterator yielding all non-empty rows in all csv files in a directory
Optional argument: regexp to filter for filenames
"""
# def getDirReader(filename):
# TODO generator that includes all generators for files in this dir  

       
        
"""
lists all rows in all csv files in a directory
Optional argument: regexp to filter for filenames
"""
#def getRowsFromDir(dirname=".", regexp= r"*.csv"):
#    os.chdir(dirname)
#    rows = []
#    for file in getFilenames(dirname, regexp):
#        rows.extend(getRowsFromFile(file))
#    return rows


if __name__ == '__main__':
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\RawData\\0" 
    filenames = list(getFilenames(dirname=RAW_DATA_PATH, regexp= r".*\.csv$"))
    print (len(filenames))
    print (filenames[0])
    rows = list(getFileReader(filenames[0]))
    print (len(rows))
    print(rows[1])  