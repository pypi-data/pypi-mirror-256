
'''
	python3 status.proc.py "_status/vows/1/status_1.py"
'''

'''
	https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
'''

from datetime import datetime
import json
import pprint

import pandas
import rich	

import ramps_trio.clouds.yahoo.read_CSV as read_CSV

def relative_path (path):
	import pathlib
	from os.path import dirname, join, normpath
	import sys

	this_directory_path = pathlib.Path (__file__).parent.resolve ()	
	return str (normpath (join (this_directory_path, path)))

	
def check_1 ():
	trend = read_CSV.start (relative_path ("yahoo-finance--BTC-USD.CSV"))
	trend_DF = pandas.DataFrame (trend)	
	

	
checks = {
	"check 1": check_1
}