

'''
	import ramps_majestic.charts.trend_side_circles as trend_side_circles
	trend_side_circles.attach (
		chart = chart,
		DF = DF
	)
'''


import numpy
import plotly.graph_objects as GO
def attach (
	chart = None, 
	DF = None
):
	chart.add_trace (
		GO.Scatter (
			x = DF ['date string'],
			y = DF ["close"],
			
			marker_color = numpy.select (
				[
					DF [ "majestic estimate" ] == "decline_move", 
					DF [ "majestic estimate" ] == "incline_move"
				], 
				[ "orange", "purple" ], 
				"rgba(0,0,0,0)"
			),
			
			mode = "markers",
			#marker_color = "black",
			yaxis = "y2",
			name = "Bubble"
		),
		row = 1, 
		col = 1
	)	