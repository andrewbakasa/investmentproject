# # TIMING ASSUMPTIONS
# timing_assumptions = {
#     'base_period': {'title': 'Base Period','value': 2021}, 
#     'construction_start_year': {'title': 'Construction start Year','value': 2021},
#     'construction_len': {'title': 'Construction length','value': 1}, 
#     'construction_year_end': {'title': 'Construction End Year','value': 2021},#one year
#     'operation_start_year': {'title': 'Operation Start Year','value': 2021}, 
#     'operation_duration': {'title': 'Operation Duration','value': 18},
#     'operation_end': {'title': 'Operation End ','value': 2039}, 
#     'number_of_months_in_a_year': {'title': 'Number of months in a year','value': 12},
#     }

# model_specifications = [
#     {'name':'LC','title':'Financial Statements Expressed in Local Currency','units':'LC'},
#     {'name':'T_LC','title':'Financial Statements Expressed in thousands of Local Currency','units':"000's LC"},
#     {'name':'M_LC','title':'Financial Statements Unit in Millions of Local Currency	Mil','units':'Mil LC'},
#     {'name':'YEAR','title':'Year','units':'Year'},
#     {'name':'YEARS','title':'Years','units':'Years'},
#     {'name':'PERCENT','title':'Percentage','units':'%'},
#     {'name':'T_TONS','title':'Thousand tons','units':"000's tons"},
#     {'name':'KG','title':'Kilograms','units':'kg'},
#     {'name':'TONS','title':'Tons','units':'tons'},
#     {'name':'M_USD','title':'Million US Dollars','units':'Mil USD'},
#     {'name':'T_USD','title':'Thousand US Dollars','units':"000's USD"},
#     {'name':'USD','title':'US Dollars','units':'USD'},
#     {'name':'NUMBER','title':'Number','units':'#'},
#     {'name':'M_CONVERSION','title':'Million to thousand conversion','units':'1000'},
#     {'name':'LITRES','title':'Litres','units':"Litres"},
#     {'name':'FLAG','title':'Flag (1= true, 0= false)','units':'flag'},
#     {'name':'SQM','title':'Square metre','units':'sqm'},
#     {'name':'SWITCH','title':'Switch','units':"switch"},
#     {'name':'NOTE','title':'Note','units':'Note'},
# ]   

# prices = {
#     'title': 'Net Sales Price:', 
#     'base_price': 4500, 
#     'change_in_price': .00, 
# }

# depreciation = {
#     'economic_life_of_machinery': {'title': 'Economic life of machinery','value': 20, 'units': 'YEARS'}, 
#     'economic_life_of_buildings': {'title': 'Economic life of buildings','value': 32, 'units': 'YEARS'},
#     'tax_life_of_machinery': {'title': 'Tax life of machinery','value': 10, 'units': 'YEARS'}, 
#     'tax_life_of_buildings': {'title': 'Tax life of buildings','value': 30, 'units': 'YEARS'},
#     'tax_life_of_soft_capital_costs': {'title': 'Tax life of soft capital costs','value': 3, 'units': 'YEARS'},
# }
# financing = {
#     'real_interest_rate': {'title': 'Real interest rate','value': .06, 'units': 'PERCENT'}, 
#     'risk_premium': {'title': 'Risk premium','value': .01, 'units': 'PERCENT'}, 
#     'num_of_installments': {'title': 'No. of installments','value': 6, 'units': 'NUMBER'},  
#     'grace_period': {'title': 'Grace period (years)','value': 0, 'units': 'YEARS'}, 
#     'repayment_starts': {'title': 'Repayment starts year','value':2022, 'units': 'YEAR'}, 
#     'equity': {'title': 'Equity (% of Investment Costs)','value': .30, 'units': 'PERCENT'}, 
#     'senior_debt': {'title': 'Senior Debt (% of Investment Costs)','value': .70, 'units': 'PERCENT'},  
# }

# working_capital = {
#     'accounts_receivable': {'title': 'Accounts receivable [% of Gross Sales]','value': 0.10, 'units': 'PERCENT'}, 
#     'accounts_payable': {'title': 'Acccounts payable (% of total input cost)','value': 0.10, 'units': 'PERCENT'}, 
#     'cash_balance': {'title': 'Cash balance  (% of gross sales)','value': 0.10, 'units': 'PERCENT'},              
# }  


# taxes = {
#     'import_duty': {'title': 'Import duty','value': 0.10, 'units': 'PERCENT'}, 
#     'sales_tax': {'title': 'Sales tax','value': .05, 'units': 'PERCENT'}, 
#     'corporate_income_tax': {'title': 'Corporate income tax','value': 0.25, 'units': 'PERCENT'}
# }

# macroeconomic_parameters = {
#     'discount_rate_equity': {'title': 'Discount Rate Equity','value': 0.12, 'units': 'PERCENT'}, 
#     'domestic_inflation_rate': {'title': 'Domestic Inflation rate','value': 0.05, 'units': 'PERCENT'},
#     'us_inflation_rate': {'title': 'US Inflation rate','value': 0.03, 'units': 'PERCENT'}, 
#     'exchange_rate': {'title': 'Exchange Rate (LC/USD - in Base Year )','value': 1.4, 'units': 'NUMBER'},
#     'dividend_payout_ratio': {'title': 'Divident Payout Ratio','value': .50, 'units': 'PERCENT'},
#     'num_of_shares': {'title': 'N# of shares','value': 10, 'units': 'NUMBER'},
# }

# feedlot_design_parameters = {
#     'num_of_feedlots': {'title': 'N# Of FeedLot','value': 5, 'units': 'NUMBER'}, 
#     'length': {'title': 'Length in meters','value': 7.5, 'units': 'NUMBER'}, 
#     'width': {'title': 'Width in meters','value': 20.0, 'units': 'NUMBER'},
#     'sqm': {'title': 'SQM covered','value': 750, 'units': 'NUMBER'},  
#     'pen_area': {'title': 'Pen-Area','value': 150, 'units': 'NUMBER'}, 
#     'sqm_per_cattle': {'title': 'SQM per cattle','value':None, 'units': 'NUMBER'},#calculated 
#     'total_cattle_per_pen_per_cycle': {'title': 'Total Cattle in one pen per cycle','value': 20, 'units': 'NUMBER'}, 
#     'num_of_months_per_cycle': {'title': 'N# of months per cycle','value': 3, 'units': 'NUMBER'},
#     'cattle_per_pen_per_year': {'title': 'Total Cattle per pen per year','value': 80, 'units': 'NUMBER'},
# }

# investment_cost = {
#     'total_land_for_pens': {'title': 'Total Land For Pens','value': 750, 'units': 'NUMBER'}, 
#     'cost_of_land_per_sqm': {'title': 'Cost of Land per SQM','value': 2, 'units': 'NUMBER'},  
#     'cost_of_machinery_per_pen': {'title': 'Cost of Machinery (Per Pen)','value': 2500, 'units': 'NUMBER'}, 
#     'cost_of_building_per_sqm': {'title': 'Cost of building per SQM','value': 10, 'units': 'NUMBER'},   
#     'total_pens': {'title': 'Total pens','value': 5, 'units': 'NUMBER'},
#     'cost_of_pen_construction': {'title': 'Cost of Unit Pen Construction','value': 1200, 'units': 'NUMBER'},
#         #for sensitivity analysis: linked sens page which then links Financing Section
#     'senior_debt_dynamic_parameter': {'title': 'Senior Debt','value': .70, 'units': 'PERCENT'}, 

#     'initial_pens_employed': {'title': 'Initial Pens Employed','value': 5, 'units': 'NUMBER'}, 
#     'pen_cattle_density': {'title': 'Pen-Cattle Density (Cattle/Pen)','value':20, 'units': 'NUMBER'}, 
#     'pen_length': {'title': 'Pen Length meters','value': 7.50, 'units': 'NUMBER'},
#     'pen_width': {'title': 'Pen Width meters','value':20.00, 'units': 'NUMBER'}, 
#     'pen_height': {'title': 'Pen Height meter','value': 2.00, 'units': 'NUMBER'},

#     'total_land_required': {'title': 'Total Land Required (hectares)','value': 1500, 'units': 'NUMBER'}, 
#     'cost_of_pens_constructed': {'title': 'Cost of pens constructed','value':None, 'units': 'T_LC'}, 
#     'cost_of_land': {'title': 'Cost of Land','value': None, 'units': 'NUMBER'},
#     'investment_cost_of_land': {'title': 'Investment cost of land','value':None, 'units': 'T_LC'}, 
#     'cif_cost_of_machinery': {'title': 'CIF cost of Machinery','value': None, 'units': 'T_USD'},
#     'investment_cost_of_buildings': {'title': 'Investment cost of buildings','value':None, 'units': 'T_LC'}, 
#     'investment_costs_over_run_factor': {'title': 'Investment Costs Over-run Factor','value': 0, 'units': 'PERCENT'},
# }

# investment_parameter_options ={
#     'cost_of_land_per_sqm':     [1.00,	 2.00,	 3.00 ,	 5.00 ,	 5.00,	 5.00],  
#     'cost_of_machinery_per_pen':[1000, 	2500, 	5000, 	5000, 	5000, 	5000], 
#     'cost_of_building_per_sqm': [10.00, 10.00, 	 8.00, 	 5.00, 	 2.00, 	 1.00], 
#     'cost_of_pen_construction': [ 1200,  1200, 	 1500, 	 2000, 	 2000 ,	 3000],
#     'senior_debt_dynamic_parameter': [.70, .70, .70, .70, .70, .70],
#     'initial_pens_employed':  [1 ,	 5, 	 20, 	 50, 	 100, 	 1000], 
#     'pen_cattle_density':   [20, 	 20, 	 20, 	 20, 	 20, 	 20] , 
#     'pen_length':           [8.00,	8.00,	8.00,	8.00,	8.00,	8.00],
#     'pen_width':            [20.00,	20.00,	20.00,	20.00,	20.00,	20.00], 
#     'pen_height':           [2.00,	2.00,	2.00,	2.00,	2.00,	2.00],
#     'total_land_required':  [1000, 	 1500, 	 5000, 	 10000, 	 50000,	 100000 ]
# }
# cattle_business_options = {
#     'minor_scale': {'heading': 'Minor Cattle Business' ,'description': 'Minor Cattle Business:  Take a salary based loan eqv $3.700, convert it into 100% EQUITY and payback in one year. Feasible anytime from now.'}, 
#     'moderate_scale': {'heading': 'Moderate Cattle Business' ,'description': 'Moderate Cattle Business: Take a salary based loan of $25,000 and payback in 5 years. This can feasible if there is confidence in banking instituion.'},
#     'bigger_scale': {'heading': 'Bigger Cattle Business' ,'description': 'Bigger Cattle Business: Heavy Investment vehicle required'},
#     'larger_scale': {'heading': 'Larger Beef Business' ,'description': 'Larger Beef Business: Heavy Investment vehicle required'},
#     'commercial_scale': {'heading': 'Commercial Beff Business' ,'description': 'Commercial Beef Business: Heavy Investment vehicle required'},
#     'global_scale': {'heading': 'Global Cattle Business' ,'description': 'Global Cattle Business: Mass Investment vehicle required'},
# }

# cost_real = {
#     #Section A---------------
#     # Number of workers and supervisors
#     'num_of_workers_per_pen': {'title': 'Number of workers per pen','value': 1, 'units': 'NUMBER'}, 
#     'cum_pens': {'title': 'Cumulative pens under harvesting','value': None, 'units': None}, 
#     'num_of_workers': {'title': 'Number of workers','value': None, 'units': 'NUMBER'},
#     'num_of_supervisors_technicians': {'title': 'Number of supervisors & technicians','value': None, 'units': 'NUMBER'},  
#     'average_num_of_workers': {'title': 'Average n# of workers','value': 5.00, 'units': 'NUMBER'}, 
#     'average_num_of_supervisors': {'title': 'Average n# of supervisors','value':None, 'units': 'NUMBER'}, 
#     #Monthly Wages and salaries
#     'total_pen_constructed': {'title': 'Total Pen Constructed','value': 5, 'units': 'NUMBER'}, 
#     'monthly_wage_per_worker': {'title': 'Monthly wage for workers','value': .3, 'units': 'T_LC'},
#     'monthly_wage_per_supervisor': {'title': 'Monthly wage for supervisors & technicians','value': .5, 'units': 'T_LC'},
    
#     #Annual Increase in real salaries
#     'annual_increase_salaries_workers': {'title': 'Annual increase in real salaries of workers','value': .03, 'units': 'PERCENT'},
#     'annual_increase_salaries_supervisors_technicians': {'title': 'Annual increase in real salaries of supervisors & technicians','value': 0.03, 'units': 'PERCENT'},
    
#     #Section B---------------
    
#     # Inputs
#     'cattle_per_pen_per_year': {'title': 'Cattle per pen per year','value': 80, 'units': 'NUMBER'},# duplicate key 
#     'food_conversion_ratio': {'title': 'Food Conversion Ratio','value': 8, 'units': 'NUMBER'}, 
#     'daily_weight_gain': {'title': 'Daily Weight Gain','value': 1.5, 'units': 'KG'},
#     'days_in_feed_lot': {'title': 'Days in Feed lot','value': 90, 'units': 'NUMBER'},  
#     'weight_at_purchase': {'title': 'Weight @ Purchase','value': 250, 'units': 'KG'}, 
#     'live_weight_gain': {'title': 'Live Weight Gain','value':135, 'units': 'KG'}, 
#     'live_weight_at_selling': {'title': 'Live Weight @ selling','value':385, 'units': 'KG'}, 
#     'qnty_of_feed_per_cattle': {'title': 'Qnty of Feed per Cattle','value': 1080, 'units': 'KG'},
#     'commercial_feed_per_pen': {'title': 'Commercial Feed per Pen','value': 86400 , 'units': 'KG'}, 
#     'dressed_weight_percent': {'title': 'Dressed Weight %','value': .55, 'units': 'PERCENT'},
#     'dressed_weight_at_selling': {'title': 'Dressed Weight @ selling','value': 211.75, 'units': 'KG'},
    

    
#     #Section C
#     #Input Prices
#     'cattle_price_per_unit': {'title': 'Cattle price per unit','value': 300, 'units': 'LC'}, #derived from senstivity
#     'cattle_feed_price_per_kg': {'title': 'Cattle Feed price per kg','value': 0.27, 'units': 'LC'},
#     'cost_of_cattle_per_pen': {'title': 'Cost of Cattle per Pen','value': 24000, 'units': 'LC'},# duplicate key 
#     'cost_of_cattle_feed_per_pen': {'title': 'Cost of Cattle Feed per Pen','value': 23328, 'units': 'LC'},
#     'total_input_costs_per_pen': {'title': 'Total Input costs per Pen','value': 47328, 'units': 'LC'},
#     'cattle_per_pen_per_year': {'title': 'Cattle per pen per year','value':80, 'units': 'NUMBER'},# duplicate key 

#     #'dressed_weight_of_cattle_at_selling': {'title': 'Dressed Weight of Cattle @ selling','value': 211.75, 'units': 'KG'},
#     'cattle_survival_rate': {'title': 'Cattle Survival rate','value': 1 , 'units': 'PERCENT'}, 
#     'tonnes_produced_per_pen_per_year': {'title': 'Tonnes Produce per pen per year','value': 16.94, 'units': 'NUMBER'},
#     'cost_of_imported_inputs_per_ton_of_beef_produced': {'title': 'Cost of imported inputs per ton of Beef produced','value': 0, 'units': 'USD'},
    
#     'cost_of_domestic_inputs_per_ton_of_beef_produced': {'title': 'Cost of domestic inputs per ton of Beef produced','value': 2794, 'units': 'LC'},
#     'cost_of_electricity_per_pen_per_annum': {'title': 'Cost Of Electricity per pen per annum','value': 100 , 'units': 'LC'}, 
#     'annual_change_in_price_of_imported_inputs': {'title': 'Annual change in price of imported inputs','value': .01, 'units': 'PERCENT'},
#     'annual_change_in_price_of_domestic_inputs': {'title': 'Annual change in price of domestic inputs','value': 0, 'units': 'PERCENT'},
#     'other_indirect_costs': {'title': 'Other Indirect Costs','value': 200, 'units': 'LC'},
# }
