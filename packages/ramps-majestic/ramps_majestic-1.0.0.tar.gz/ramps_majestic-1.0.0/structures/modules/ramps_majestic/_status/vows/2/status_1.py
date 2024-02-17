
'''
	python3 status.proc.py "_status/vows/2/status_1.py"
'''

'''
	https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
'''

from datetime import datetime
import json
import pprint

import pandas
import rich	

import ramps_majestic
import ramps_majestic.victory_multiplier.purchase_treasure_at_inclines as purchase_treasure_at_inclines_VM	
import ramps_majestic.victory_multiplier.purchase_treasure_over_span as purchase_treasure_over_span_VM
import ramps_majestic.furniture.CSV.read as read_CSV
	

def relative_path (path):
	import pathlib
	from os.path import dirname, join, normpath
	import sys

	this_directory_path = pathlib.Path (__file__).parent.resolve ()	
	return str (normpath (join (this_directory_path, path)))

def check_1 ():
	
	'''
		This parses the data from the CSV.
	'''
	trend = read_CSV.start (relative_path ("yahoo-finance--SPXU.csv"))	
	trend_DF = pandas.DataFrame (trend)	
	
	enhanced_trend_DF = ramps_majestic.calc (
		trend_DF,
		period = 14,
		multiplier = 3
	)
	enhanced_list = enhanced_trend_DF.to_dict ('records')

	
	'''
		This calculates the multipliers
	'''
	treasure_at_inclines_VM = purchase_treasure_at_inclines_VM.calc (enhanced_trend_DF)
	rich.print_json (data = treasure_at_inclines_VM)	
	assert (treasure_at_inclines_VM ["treasure purchase victory multiplier"] == 0.9198514681826051)
	
	open_price_at_spans_VM = purchase_treasure_over_span_VM.calc (enhanced_trend_DF)
	assert (open_price_at_spans_VM == 0.5551523947750363)
	
	
	ramps_majestic.chart_the_data (
		enhanced_trend_DF,
		treasure_at_inclines_VM
	)
	
	
	
checks = {
	"check 1": check_1
}