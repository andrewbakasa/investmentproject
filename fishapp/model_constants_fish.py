""" 
IN FUTURE VARIABLE DEPENDS:
1. user
2. country
3. selected model
4..any other logic (AI) etc


"""

prices_fish = {
    'title': 'Net Sales Price:', 
    'base_price': 4500, 
    'change_in_price': .00, 
}

depreciation_fish = {
    'economic_life_of_machinery': {'title': 'Economic life of machinery','value': 20, 'units': 'YEARS'}, 
    'economic_life_of_buildings': {'title': 'Economic life of buildings','value': 32, 'units': 'YEARS'},
    'tax_life_of_machinery': {'title': 'Tax life of machinery','value': 10, 'units': 'YEARS'}, 
    'tax_life_of_buildings': {'title': 'Tax life of buildings','value': 30, 'units': 'YEARS'},
    'tax_life_of_soft_capital_costs': {'title': 'Tax life of soft capital costs','value': 3, 'units': 'YEARS'},
}




investment_cost_fish = {
    'total_land_for_tanks': {'title': 'Total Land For Tanks','value': 0, 'units': 'NUMBER'}, 
    'cost_of_land_per_sqm': {'title': 'Cost of Land per SQM','value': 0, 'units': 'LC'},  
    'cost_of_machinery_per_tank': {'title': 'Cost of Machinery (Per Tank)','value': 100, 'units': 'LC'}, 
    'cost_of_building_per_sqm': {'title': 'Cost of building per SQM','value': 0, 'units': 'LC'},   
    'total_tanks': {'title': 'Total Tanks','value': 10, 'units': 'NUMBER'},
    'cost_of_unit_tank': {'title': 'Cost of Unit Tank','value': 700, 'units': 'LC'},
        #for sensitivity analysis: linked sens page which then links Financing Section
    'senior_debt_dynamic_parameter': {'title': 'Senior Debt','value': 0, 'units': 'PERCENT'}, 

    'initial_tanks_employed': {'title': 'Initial Tanks Employed','value': 10, 'units': 'NUMBER'}, 
    'fish_density': {'title': 'Fish-Tank Density (Fish/Tank)','value':2000, 'units': 'NUMBER'}, 
    'tank_length': {'title': 'Tank Length meters','value': 4.57, 'units': 'NUMBER'},
    'tank_width': {'title': 'Tank Width meters','value':4.57, 'units': 'NUMBER'}, 
    'tank_depth': {'title': 'Tank Depth meter','value': 0.91, 'units': 'NUMBER'},

    'total_land_required': {'title': 'Total Land Required (hectares)','value': 0, 'units': 'NUMBER'}, 
    #'cost_of_tanks': {'title': 'Cost of Tanks','value':None, 'units': 'T_LC'},
    'cost_of_tanks_constructed': {'title': 'Cost of Tanks constructed','value':None, 'units': 'T_LC'},
    'cost_of_land': {'title': 'Cost of Land','value': None, 'units': 'T_LC'},
    'investment_cost_of_land': {'title': 'Investment cost of land','value':None, 'units': 'T_LC'}, 
    'cif_cost_of_machinery': {'title': 'CIF cost of Machinery','value': None, 'units': 'T_USD'},
    'investment_cost_of_buildings': {'title': 'Investment cost of buildings','value':None, 'units': 'T_LC'}, 
    'investment_costs_over_run_factor': {'title': 'Investment Costs Over-run Factor','value': 0, 'units': 'PERCENT'},
}
# tank_design_parameters = {
#     'num_of_tanks': {'title': 'N# Of FeedLot','value': 5, 'units': 'NUMBER'}, #from database
#     'length': {'title': 'Length in meters','value': 3.60, 'units': 'NUMBER'}, 
#     'width': {'title': 'Width in meters','value': 3.60, 'units': 'NUMBER'},
#     'sqm': {'title': 'SQM covered by Tanks','value': 0, 'units': 'NUMBER'},  #Derived
#     'depth': {'title': 'Depth in meters','value': .9, 'units': 'NUMBER'},
#     'density_per_cubic_metre': {'title': 'Density/ [cm]','value': 150, 'units': 'NUMBER'}, 
#     'volume_of_water': {'title': 'Volume Of Water/tank','value':None, 'units': 'LITRES'},#calculated 
#     'total_fish_per_tank_per_cycle': {'title': 'Total Fish in one tank per cycle','value': 2000, 'units': 'NUMBER'}, 
#     'num_of_months_per_cycle': {'title': 'N# of months per cycle','value': 6, 'units': 'NUMBER'},
#     'fish_per_tank_per_year': {'title': 'Total Fish per tank per year','value': 7000, 'units': 'NUMBER'},
# }

       

investment_parameter_options_fish ={
    'cost_of_land_per_sqm':     [0,     0,       50.00,	  15.00,	 40.00 ,	 40.00],  
    'cost_of_machinery'   :     [0, 	0, 	     100, 	  200, 	     100, 	     200], 
    'cost_of_building_per_sqm': [0,     2.00, 	 10.00,   30.00, 	 10.00,     10.00], 
    'cost_of_unit_tank':        [ 700,  700, 	 700, 	   700, 	 1350 ,	     1350],
    'senior_debt_dynamic_parameter': [.0, .0, .50, .50, .70, .70],
    'initial_tanks_employed':  [10 ,	 20, 	 50, 	 50, 	 50, 	 500], 
    'fish_density':           [2000, 	 2000, 	 2000, 	 2000, 	 3500, 	 3500] , 
    'tank_length':           [4.57,	4.57,	4.57,	4.57,	3.60,	3.60],
    'tank_width':            [4.57,	4.57,	4.57,	4.57,	3.60,	3.60], 
    'tank_depth':           [0.91,	0.91,	0.91,	0.91,	1.20,	1.20],
    'total_land_required':  [0, 	 0, 	 3000, 	 2000, 	 10000,	 10000 ],
    'cost_of_machinery_per_tank':  [100, 	 100, 	 300, 	 500, 	 1000,	 10000 ]
    
}
 
 								



#------dynamic from database
fish_business_options = {
    'my_option': {'heading': 'My Option Business' ,'description': 'My Option Business:  .....'},  
    'minor_scale': {'heading': 'Minor Backyard Scale' ,'description': 'Minor Backyard Scale:  Take a salary based loan eqv $3.700, convert it into 100% EQUITY and payback in one year. Feasible anytime from now.'}, 
    'moderate_scale': {'heading': 'Moderate Backyard Scale' ,'description': 'Moderate Backyard Scale: Take a salary based loan of $25,000 and payback in 5 years. This can feasible if there is confidence in banking instituion.'},
    'bigger_scale': {'heading': 'Full Backyard Scale' ,'description': 'Full Backyard Scale: Heavy Investment vehicle required'},
    'larger_scale': {'heading': 'Bigger Scale' ,'description': 'Bigger Scale: Heavy Investment vehicle required'},
    'commercial_scale': {'heading': 'Ultimate Scale' ,'description': 'Ultimate Scale: Heavy Investment vehicle required'},
    'global_scale': {'heading': 'Full Scale' ,'description': 'Full Scale: Mass Investment vehicle required'},
}

cost_real_fish = {
    #Section A---------------
    # Number of workers and supervisors
    'num_of_workers_per_tank': {'title': 'Number of workers per tank','value': 0.0833, 'units': 'NUMBER'}, 
    'cum_tanks': {'title': 'Cumulative pens under harvesting','value': None, 'units': None}, 
    'num_of_workers': {'title': 'Number of workers','value': None, 'units': 'NUMBER'},
    'num_of_supervisors_technicians': {'title': 'Number of supervisors & technicians','value': None, 'units': 'NUMBER'},  
    'average_num_of_workers': {'title': 'Average n# of workers','value': 5.00, 'units': 'NUMBER'}, 
    'average_num_of_supervisors': {'title': 'Average n# of supervisors','value':None, 'units': 'NUMBER'}, 
    #Monthly Wages and salaries
    'total_pen_constructed': {'title': 'Total Pen Constructed','value': 5, 'units': 'NUMBER'}, 
    'monthly_wage_per_worker': {'title': 'Monthly wage for workers','value': .3, 'units': 'T_LC'},
    'monthly_wage_per_supervisor': {'title': 'Monthly wage for supervisors & technicians','value': .5, 'units': 'T_LC'},
    
    #Annual Increase in real salaries
    'annual_increase_salaries_workers': {'title': 'Annual increase in real salaries of workers','value': .03, 'units': 'PERCENT'},
    'annual_increase_salaries_supervisors_technicians': {'title': 'Annual increase in real salaries of supervisors & technicians','value': 0.03, 'units': 'PERCENT'},
    
    #Section B---------------
    
    # Inputs
    'food_conversion_ratio': {'title': 'Food Conversion Ratio','value': 8, 'units': 'NUMBER'}, 
    'daily_weight_gain': {'title': 'Daily Weight Gain','value': 1.7, 'units': 'G'},
    'days_in_tank': {'title': 'Days in Tank','value': 180, 'units': 'NUMBER'}, 
    'qnty_of_feed_per_tank_cycle': {'title': 'Qnty of Feed per Tank cycle','value': 300, 'units': 'KG'},
    'qnty_of_feed_per_fish_cycle': {'title': 'Qnty of Fish Feed per cycle','value': .2, 'units': 'KG'}, 
    'commercial_feed_per_tank': {'title': 'Qnty of Commercial Feed per tank','value': 300 , 'units': 'KG'}, 
    'fish_weight_at_selling': {'title': 'Fish Weight @ selling','value': 300, 'units': 'G'},
    

    
    #Section C
    #Input Prices
    'fingerlings_price_per_1000_units': {'title': 'Fingerlings price per 1000 units','value': 100, 'units': 'LC'}, #derived from senstivity
    'fish_feed_price_per_kg': {'title': 'Fish Feed price per kg','value': 0.80, 'units': 'LC'},
    'cost_of_fish_per_tank': {'title': 'Cost of Fingerlins per Tank','value': 24000, 'units': 'LC'},# duplicate key 
    'cost_of_fish_feed_per_tank': {'title': 'Cost of Fish Feed per Tank','value': 23328, 'units': 'LC'},
    'total_input_costs_per_tank': {'title': 'Total Input costs per Tank','value': 47328, 'units': 'LC'},
    'fish_per_tank_per_year': {'title': 'Fish per tank per year','value':7000, 'units': 'NUMBER'},# derived key 
     'total_fish_per_tank_per_cycle': {'title': 'Fish per tank per cycle','value':2000, 'units': 'NUMBER'},# duplicate key

    'fingerlings_price_per_1000_units': {'title': 'Fingerlings price per 1000 units','value': 100, 'units': 'LC'},
    'fingerlings_survival_rate': {'title': 'Fingerlings Survival rate','value': .80 , 'units': 'PERCENT'}, 
    'tonnes_produced_per_tank_per_year': {'title': 'Tonnes Produce per tank per year','value': 16.94, 'units': 'NUMBER'},
    'cost_of_imported_inputs_per_ton_of_fish_produced': {'title': 'Cost of imported inputs per ton of Fish produced','value': 0, 'units': 'USD'},
    
    'cost_of_domestic_inputs_per_ton_of_fish_produced': {'title': 'Cost of domestic inputs per ton of Fish produced','value': 2794, 'units': 'LC'},
    'cost_of_electricity_per_tank_per_annum': {'title': 'Cost Of Electricity per tank per annum','value': 100 , 'units': 'LC'}, 
    'annual_change_in_price_of_imported_inputs': {'title': 'Annual change in price of imported inputs','value': .01, 'units': 'PERCENT'},
    'annual_change_in_price_of_domestic_inputs': {'title': 'Annual change in price of domestic inputs','value': 0, 'units': 'PERCENT'},
    'other_indirect_costs': {'title': 'Other Indirect Costs','value': 200, 'units': 'LC'},
}