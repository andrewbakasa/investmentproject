from django.db import models

from investments_appraisal.models import UserModel

# Create your models here.
#-------------OPTIONS: BEEF
class FeedlotDesignParameters(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    num_of_feedlots =  models.IntegerField(default=1)
    length =  models.DecimalField(decimal_places=2, max_digits=10 , default=7.5)
    width =  models.DecimalField(decimal_places=2, max_digits=10, default=7.5)
    #sqm =  models.DecimalField(decimal_places=2, max_digits=10 ,default=2500)
    #pen_area =  models.DecimalField(decimal_places=2, max_digits=10, default=2500)
    sqm_per_cattle =  models.DecimalField(decimal_places=2, max_digits=10, default=10)
    total_cattle_per_pen_per_cycle =  models.IntegerField(default=20)
    num_of_months_per_cycle =  models.IntegerField(default=3)
    #cattle_per_pen_per_year =  models.IntegerField(default=80)


    construction_cost_per_pen =  models.DecimalField(decimal_places=2, max_digits=15, default=1000)
    machinery_cost_per_pen =  models.DecimalField(decimal_places=2,max_digits=15, default=1200)
    building_cost_per_sqm =  models.DecimalField(decimal_places=2, max_digits=15,default=10)
    total_land_sqm =  models.DecimalField(decimal_places=2, max_digits=15,default=1000)
    cost_of_land_per_sqm =  models.DecimalField(decimal_places=2, max_digits=15,default=1)




 
#-------------OPTIONS: BEEF
class InvestmentCostFeedLots(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    total_land_for_pens = models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_land_per_sqm =  models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_machinery_per_pen =  models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_building_per_sqm =  models.DecimalField(decimal_places=2, max_digits=10)
    total_pens =  models.IntegerField(default=5)
    cost_of_pen_construction =  models.DecimalField(decimal_places=2, max_digits=10)
    senior_debt_dynamic_parameter =  models.DecimalField(decimal_places=2, max_digits=10)
    initial_pens_employed =  models.IntegerField(default=1)
    cattle_per_pen_per_year =  models.IntegerField(default=1)
   
    
    #pen_length =  models.DecimalField(decimal_places=2, max_digits=10)# duplication
    ##pen_width =  models.DecimalField(decimal_places=2, max_digits=10)# duplication
    #pen_height =  models.DecimalField(decimal_places=2, max_digits=10)# duplication
    total_land_required =  models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_pens_constructed =  models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_land =  models.DecimalField(decimal_places=2, max_digits=10)
    investment_cost_of_land =  models.DecimalField(decimal_places=2, max_digits=10)
    cif_cost_of_machinery =  models.DecimalField(decimal_places=2, max_digits=10)
    investment_cost_of_buildings =  models.DecimalField(decimal_places=2, max_digits=10)
    investment_costs_over_run_factor =  models.DecimalField(decimal_places=2, max_digits=10)


   
#-------------OPTIONS: BEEF
class InvestmentParameterOptions(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    option_name =models.CharField(max_length=200, null=False) #minor_scale,                            moderate_scale
    option_heading =models.CharField(max_length=200, null=False)#Minor Cattle Business,                Moderate Cattle Business...
    option_title =models.CharField(max_length=200, null=False)#Minor Cattle Business:  Take a salar,   Moderate Cattle Business: Take a sa...
    cost_of_land_per_sqm = models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_machinery_per_pen =  models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_building_per_sqm =  models.DecimalField(decimal_places=2, max_digits=10)
    cost_of_pen_construction =  models.DecimalField(decimal_places=2, max_digits=10)
    senior_debt_dynamic_parameter =  models.DecimalField(decimal_places=2, max_digits=10)
    initial_pens_employed =  models.IntegerField(default=1)
    
    pen_cattle_density =  models.DecimalField(decimal_places=2, max_digits=10)
    pen_length =  models.DecimalField(decimal_places=2, max_digits=10)
    pen_width =  models.DecimalField(decimal_places=2, max_digits=10)
    pen_height =  models.DecimalField(decimal_places=2, max_digits=10)
    total_land_required =  models.DecimalField(decimal_places=2, max_digits=10)
   
  
#-------------OPTIONS: BEEF
class CostReal(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    num_of_workers_per_pen = models.DecimalField(decimal_places=2, max_digits=10)
    #cum_pens =  models.DecimalField(decimal_places=2, max_digits=10) #derived
    #num_of_workers =  models.DecimalField(decimal_places=2, max_digits=10)#derived
    #num_of_supervisors_technicians =  models.DecimalField(decimal_places=2, max_digits=10) #dervied
    #average_num_of_workers =  models.DecimalField(decimal_places=2, max_digits=10)#derived
    #average_num_of_supervisors =  models.DecimalField(decimal_places=2, max_digits=10)#derived
    
    total_pen_constructed =  models.IntegerField()
    monthly_wage_per_worker =  models.DecimalField(decimal_places=2, max_digits=10)
    monthly_wage_per_supervisor =  models.DecimalField(decimal_places=2, max_digits=10)
    
    annual_increase_salaries_workers =  models.DecimalField(decimal_places=2, max_digits=10)
    annual_increase_salaries_supervisors_technicians =  models.DecimalField(decimal_places=2, max_digits=10)
       
    cattle_per_pen_per_year =  models.IntegerField()#duplicate
    food_conversion_ratio =  models.DecimalField(decimal_places=2, max_digits=10)
    daily_weight_gain =  models.DecimalField(decimal_places=2, max_digits=10)
    days_in_feed_lot =  models.DecimalField(decimal_places=2, max_digits=10)
    weight_at_purchase =  models.DecimalField(decimal_places=2, max_digits=10)#duplicate
    live_weight_gain =  models.DecimalField(decimal_places=2, max_digits=10)
   
    live_weight_at_selling =  models.DecimalField(decimal_places=2, max_digits=10)
    qnty_of_feed_per_cattle =  models.DecimalField(decimal_places=2, max_digits=10)
    commercial_feed_per_pen =  models.DecimalField(decimal_places=2, max_digits=10)
    dressed_weight_percent =  models.DecimalField(decimal_places=2, max_digits=10)
    dressed_weight_at_selling =  models.DecimalField(decimal_places=2, max_digits=10)
   
   
    cattle_price_per_unit =  models.DecimalField(decimal_places=2, max_digits=10)
    cattle_feed_price_per_kg =  models.DecimalField(decimal_places=2, max_digits=10)
    #cost_of_cattle_per_pen =  models.DecimalField(decimal_places=2, max_digits=10)# derived
    #cost_of_cattle_feed_per_pen =  models.DecimalField(decimal_places=2, max_digits=10) derived
    #total_input_costs_per_pen =  models.DecimalField(decimal_places=2, max_digits=10)# derived
     
    #cattle_per_pen_per_year =  models.IntegerField() derived#
    cattle_survival_rate =  models.DecimalField(decimal_places=2, max_digits=10)
    #tonnes_produced_per_pen_per_year =  models.DecimalField(decimal_places=2, max_digits=10)
    #cost_of_imported_inputs_per_ton_of_beef_produced =  models.DecimalField(decimal_places=2, max_digits=10) derived
    #cost_of_domestic_inputs_per_ton_of_beef_produced =  models.DecimalField(decimal_places=2, max_digits=10)# derived
     
    cost_of_electricity_per_pen_per_annum =  models.DecimalField(decimal_places=2, max_digits=10)
    annual_change_in_price_of_imported_inputs =  models.DecimalField(decimal_places=2, max_digits=10)
    annual_change_in_price_of_domestic_inputs =  models.DecimalField(decimal_places=2, max_digits=10)
    other_indirect_costs =  models.DecimalField(decimal_places=2, max_digits=10)
 