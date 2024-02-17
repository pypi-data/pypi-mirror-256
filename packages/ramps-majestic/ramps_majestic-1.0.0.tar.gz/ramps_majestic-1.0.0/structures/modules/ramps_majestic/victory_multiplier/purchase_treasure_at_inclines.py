

'''
	import ramps_majestic.victory_multiplier.purchase_treasure_at_inclines as purchase_treasure_at_inclines_VM
	purchase_treasure_at_inclines_VM.calc (data)
'''


'''
	description:
		This adds..
'''

'''
	agenda: 
		{
			"ramp victory percentage": "",
			"hold victory percentage": ""
		}
'''



import rich
from fractions import Fraction
def calc (
	DF,
	include_last_change = False
):	
	relevant = []
	
	'''
		find incline_move signal to decline_move signal multiplier.
	'''	
	last_index = DF.iloc[-1].name
	for index, row in DF.iterrows ():
		incline = row ['majestic incline']
		decline = row ['majestic decline']
			
		if (
			incline == "yes" or 
			decline == "yes" or
			(include_last_change and last_index == index)
		):
			if (last_index == index):
				last = "yes"
			else:
				last = "no"
		
			relevant.append ({
				"date string": row ["date string"],
				"majestic incline": incline,
				"majestic decline": decline,
				"open": row ["open"],
				"change": None,
				"aggregate change": None,
				"last": last
			})
			
			
	
	aggregate_change = []
	last_index = len (relevant) - 1
	s = 1
	while s <= last_index:
		was_incline_start = (
			relevant [s - 1] ["majestic decline"] == "no" and
			relevant [s - 1] ["majestic incline"] == "yes"
		)
	
		is_decline_start = (
			relevant [s] ["majestic decline"] == "yes" and
			relevant [s] ["majestic incline"] == "no"
		)
		
		is_last = relevant [s] ["last"] == "yes"
	
		if (was_incline_start and (is_decline_start or is_last)):
			the_change = (relevant [s] ["open"]) / relevant [s - 1] ["open"]
			
			relevant [s] ["change"] = the_change
	
			if (len (aggregate_change) == 0):
				the_aggregate_change = the_change
				aggregate_change.append (the_aggregate_change)
			
			else:
				the_aggregate_change = aggregate_change [ len (aggregate_change) - 1 ] * the_change
				aggregate_change.append (the_aggregate_change)
				
			relevant [s] ["aggregate change"] = the_aggregate_change
			
	
		s += 1
		
	#rich.print_json (data = relevant)
	

	return {
		"treasure purchase victory multiplier": float (
			aggregate_change [ len (aggregate_change) - 1 ]
		),
		"relevant": relevant
	}