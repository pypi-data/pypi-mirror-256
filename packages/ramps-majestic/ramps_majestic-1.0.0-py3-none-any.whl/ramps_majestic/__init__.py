



'''
	based on:
		https://stackoverflow.com/questions/44935269/supertendency-code-using-pandas-python
'''


from ._clique import clique


'''
	pivot indicates a band change.
	
	The place 1 place after the pivot
	is where the purchase or sale event
	can occur at the open price.
	
		"majestic incline": "yes",
		"majestic decline": "no",
'''

'''
	import ramps_majestic
	enhanced_tendency_DF = majestic.calc ([{
		"high": "",
		"low": "",
		"open": "",
		"close": ""
	}])	
'''



from ramps_majestic.tendencies.majestic import calc


'''
	This charts the data
'''
import rich

import ramps_majestic
import ramps_majestic.victory_multiplier.purchase_treasure_at_inclines as purchase_treasure_at_inclines_VM	
import ramps_majestic.victory_multiplier.purchase_treasure_over_span as purchase_treasure_over_span_VM
import ramps_majestic.furniture.CSV.read as read_CSV
def chart_the_data (
	enhanced_trend_DF = None,
	treasure_at_inclines_VM = None
):
	import ramps_majestic.charts.VLOCH as VLOCH
	chart = VLOCH.show (
		DF = enhanced_trend_DF
	)
	import ramps_majestic.charts.majestic_line as majestic_line
	majestic_line.attach (
		chart = chart,
		DF = enhanced_trend_DF
	)	
	import ramps_majestic.charts.shapes.vline as vline_shape	
	import ramps_majestic.charts.annotations.vline as vline_annotation
	relevant = treasure_at_inclines_VM ["relevant"]
	for place in relevant:
		multiplier = "()"
		if (type (place ["change"]) == float):
			multiplier = "(" + str (round (place ["change"], 3)) + ")";
		
		open = place ["open"]
	
		vline_shape.show (
			chart,
			DF = enhanced_trend_DF,
			x = place ["date string"]
		)
		vline_annotation.show (
			chart,
			DF = enhanced_trend_DF,
			x = place ["date string"],
			
			text = f"{ open } { multiplier }"
		)

	#rich.print_json (data = treasure_at_inclines_VM ["relevant"])
	
	columns = list (relevant[0].keys())

	import plotly.graph_objects as go
	chart.append_trace ( 
		go.Table (
			header = dict(values=columns),
			cells = dict(values=list(zip(*[data.values() for data in relevant])))
		),
		row = 2,
		col = 1
	)
	
	chart.show ()