#new
import copy
import math
import os

import pandas as pd

from investments_appraisal.whatif import get_data_table_sensitivity_in_parrallel, get_sensitivity_gradient
from re import A, L
from django.utils import translation
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str, force_str
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.utils.formats import get_format, number_format
from django.utils.text import capfirst, get_text_list, format_lazy
from io import StringIO, BytesIO


from tempfile import NamedTemporaryFile
import numpy as np
import numpy_financial as npf

class BaseModel():
  
   #Flags
    flags = {
        'YEAR': {'title': 'Years','units': 'Year'}, 
        'PS': {'title': 'Project start','units': 'flag'},
        'CP': {'title': 'Construction period flag','units':'flag'}, 
        'LPP': {'title': 'Loan principle repayment','units': 'flag'},
        'OP': {'title': 'Operating period','units': 'flag'},
        'RES': {'title': 'Residuals','units': 'flag'}, 
            
    }
    
    myworboook = None
    

    def update(self, param_dict):
        """
        Update parameter values
        """
        for key in param_dict:
            setattr(self, key, param_dict[key])
    

    def __init__(self, model_specifications=None, timing_assumptions=None, 
                 prices= None, working_capital=None,
                 financing=None, taxes=None, 
                 macroeconomic_parameters=None,  depreciation=None, 
                 description_font=None, description_font2=None,):
        
        # self.is_bound = data is not None or files is not None # false/True
        self.model_specifications = model_specifications
        self.timing_assumptions = timing_assumptions
        self.prices = prices
        self.working_capital = working_capital
        self.financing = financing
        self.taxes = taxes
        self.macroeconomic_parameters = macroeconomic_parameters
        self.depreciation = depreciation
        self.financing = financing

        if description_font is not None:
            self.description_font= description_font

        if description_font2 is not None:
            self.description_font2= description_font2
        #add i think this will work
        self.financing['repayment_starts']['value']=self.timing_assumptions['base_period']['value'] + self.financing['grace_period']['value']
     
        #initial calculate this values
        #self._cal_metrix()--- removed to be implemented inside derived class
    def __str__(self):
        """
        String representation of Class object inputs var
        """
        return str(vars(self)) 
    def write_sens_data(self):
        #-------------save data---------------
           
        workpath =  os.path.dirname(os.path.abspath(__file__))
        file_name= os.path.join(workpath, 'data/sens_data.csv')   

        if hasattr(self,'sens_dict'):
            results_df=self.get_sens_results_df(self.sens_dict)
            results_df.to_csv(file_name, index = False, header=True)
      
     
    def get_sens_results_df(self,dict_):
        #print(new_dict_of_dict)
        #k={
        #1. 'price':{'df':df, 'params'....}
        #2. 'survival_rate':{'df':df, 'params'....}
        # }
    
        dfs = []    
        #for r in results:
        for key in dict_.keys():
            var=key
            df = dict_[key]['df'] 
            df['parameter']=var
            params =dict_[key]['params']
            for j in params.keys():
                #take the values if not in imput already
                if j not in df.columns:
                    df[j]=params[j]
            
            dfs.append(df)

        results_df = pd.concat(dfs)
        return results_df
    #--------------------------------------------------
    def _sen_parameter_generator(self, point_x, var_x):
        list_ =[]
        if hasattr(self,'sens_input_dict'):
            sens_var= var_x.split("sens_",1)[1].strip()
            if sens_var in self.sens_input_dict.keys():
                list_=list(self.sens_input_dict[sens_var]['list'])
       
       
        #check x_npv_0 in included-------
        x_npv_0=None
        included=-1
        sens_var= var_x.split("sens_",1)[1].strip()
        if hasattr(self,'sens_dict'):
            if sens_var in self.sens_dict.keys():
                if 'x_npv_0' in self.sens_dict[sens_var].keys():
                    x_npv_0 = self.sens_dict[sens_var]['x_npv_0'] 
                if 'included' in self.sens_dict[sens_var].keys():
                    included = self.sens_dict[sens_var]['included'] 
        
        index_npv_zero=-1
        if x_npv_0!=None and included!=-1:
            if not (x_npv_0 in list_):
                    list_.append(x_npv_0)
            
            if x_npv_0!=point_x:
                index_npv_zero = list_.index(x_npv_0) + 1
                
        list_.sort()
        if hasattr(self,'sens_dict'):
            if sens_var in self.sens_dict.keys():
                list_= self.sens_dict[sens_var]['df'][sens_var].tolist()
               
                l= [round(x,5) for x in list_]
                if x_npv_0!=None and included!=-1:
                    if round(x_npv_0,5) in l:
                        index_npv_zero = l.index(round(x_npv_0,5)) + 1
                    else:
                        xx= list(np.abs(np.array(list_)-x_npv_0))
                        xx =[round(x,5) for x in xx]
                        xp= np.argmin(np.array(xx))
                        index_npv_zero=xp+1   
                   
                
        #get index of base value
        if  (point_x in list_):
            index_of_base_value = list_.index(point_x) + 1
        else:
            index_of_base_value=-1

        # 
       
        return list_, index_of_base_value,index_npv_zero
    def _get_loan_principal_repayment_bounds(self,):
        # -    1   1   1   1  1   -   -   -
        #     
        found_lb= False
        lbound= None
        ubound= None
        
        base_period= int(self.timing_assumptions['base_period']['value'])
        #vara =   int(self.financing['repayment_starts']['value'])
        repayment_starts=self.timing_assumptions['base_period']['value'] + self.financing['grace_period']['value']
        vara =   int(repayment_starts)
      
        varb =  int(repayment_starts) + int(self.financing['num_of_installments']['value'])  -1
        operation_end= int(self.timing_assumptions['operation_end']['value'])
        
        list_ =[]
        continue_flag= True
        ONES_found= False
        period_iter=base_period
       
        while continue_flag:
            
            span_num = period_iter - base_period
            if not(period_iter < vara  or period_iter > varb):
                # Repayment period
                ONES_found = True
                found_lb= True
                if lbound==None:
                    #latch the first
                    lbound= span_num
                if ubound==None:
                    ubound=span_num 
                else:
                    #continue updating
                    ubound=span_num 
            else:
                #outside repayment perion
                #0 preceding 1 means repayment done
                if ONES_found == True:
                    continue_flag=False
            # premature exist no period found        
            if period_iter >operation_end:
                continue_flag=False

            period_iter += 1   
        return lbound, ubound, found_lb

    def _get_number_formats(self, x):
        #print(isinstance(x,str),type(x)==str )
        if type(x)==str:
            if x.upper() =='PERCENT':
                return '0%'
            elif x.upper()=='NUMBER':
                return '_(* #,##0.0_);_(* \(#,##0.0\);_(* "-"??_);_(@_)' 
            else:
                return 'General' 
        else:
            return 'General'              
  
      
      
      
    def _metric_workingCapital(self):
        #problematic.......
       

        #Accounts receivable [% of Gross Sales]
        arogs_list= [x*self.accounts_receivable for x in self.gsr_list]
        setattr(self, 'arogs_list', self.clean_inf_array(arogs_list))
        #print('arogs_list',arogs_list)
     
        #Acccounts payable (% of total input cost)
        apotic_list= [x*self.accounts_payable for x in self.tic_n_list]
        setattr(self, 'apotic_list', self.clean_inf_array(apotic_list))
        #print('apotic_list',apotic_list)

        #Cash balance  (% of gross sales)
        cbogs_list= [x*self.cash_balance for x in self.gsr_list]
        setattr(self, 'cbogs_list', self.clean_inf_array(cbogs_list))
     
        #Change in A/R
        ciar_list= list(self._accumulate_change_in(self.arogs_list))
        setattr(self, 'ciar_list', self.clean_inf_array(ciar_list))
        
        #Change in A/P
        ciap_list= list(self._accumulate_change_in(self.apotic_list))
        setattr(self, 'ciap_list', self.clean_inf_array(ciap_list))
        #print('ciap_list',ciap_list)
        #Change in cash balance
        cicb_list= list(self._accumulate_change_in_CB(self.cbogs_list))
        setattr(self, 'cicb_list', self.clean_inf_array(cicb_list))
    def _metric_loanSchedule(self):
       
        
      
        #US inflation
        us_inflation_rate_list= [self.us_inflation_rate for x in self.tp_list]
        setattr(self, 'us_inflation_rate_list', us_inflation_rate_list)
        nominal_interest_rate_list= list(self._accumulate_nominal_interest_rate(self.us_inflation_rate_list,
                                    self.real_interest_rate,self.risk_premium))
        setattr(self, 'nominal_interest_rate_list', self.clean_inf_array(nominal_interest_rate_list))

        #Domestic
        domestic_inflation_rate_list= [self.domestic_inflation_rate for x in self.tp_list]
        setattr(self, 'domestic_inflation_rate_list', domestic_inflation_rate_list)
        nominal_interest_rate_lc_list= list(self._accumulate_nominal_interest_rate_lc(self.domestic_inflation_rate_list,
                                    self.discount_rate_equity))
        setattr(self, 'nominal_interest_rate_lc_list', self.clean_inf_array(nominal_interest_rate_lc_list))

        #upper_bound= (self.repayment_starts + self.num_of_installments - self.grace_period-1)
        upper_bound= (self.repayment_starts + self.num_of_installments -1)
        #upper bound questionable effect of grace period..........

        # print('self.repayment_starts',self.repayment_starts)
        # print('upper_bound',upper_bound)
        # print(f'range allowed : {self.start_year} <====> {upper_bound}')
        #ERROR SOLVED????? 22 May 2022 1805HR: Raining and cold, programming in blanked @ 08 Mopani Road morningside Mutare
        # relaced start year with repayment_starts
        loan_principal_repayment_flag_list=[0 if x < self.repayment_starts or x > upper_bound else 1 for x in self.tp_list]#dynamic later
        # print('time period',self.tp_list)
        # print('loan repayment',loan_principal_repayment_flag_list)

        setattr(self, 'loan_principal_repayment_flag_list', loan_principal_repayment_flag_list)
        
        construction_period_flag_list=[0 if x > self.construction_year_end  else 1 for x in self.tp_list]#dynamic later
        setattr(self, 'construction_period_flag_list', construction_period_flag_list)
       
        # self.financing['equity']['value']

        # self.financing['senior_debt']['value']
      
        # OPENING INVENTORY			
		# 	Real interest rate
		# 	Risk premium
		# 	US Inflation rate
		# 	Nominal Interest Rate
		# 	Local Inflation rate
		# 	Nominal Interest Rate (Local)
			
        # SUPPLIERS CREDIT			
        #             US Price Index
        #             No. of installments
        #             Loan principle repayment

       
        # Loan Repayment Schedule			
		# 	Beginning Debt
           # 	Loan disbursement
       
        loan_disbursement_list= [x for x in self.senior_debt_contr_investments]
        setattr(self, 'loan_disbursement_list', loan_disbursement_list)
        total_loan_disbursed =np.sum(self.loan_disbursement_list)

        principal_paid_list= [total_loan_disbursed*x/self.num_of_installments if self.num_of_installments !=0 else 0 for x in self.loan_principal_repayment_flag_list]
        setattr(self, 'principal_paid_list', principal_paid_list)
        beggining_debt_list= list(self._accumulate_beginning_debt(self.loan_disbursement_list, 
                                                                self.principal_paid_list))
        
        setattr(self, 'beggining_debt_list', self.clean_inf_array(beggining_debt_list))
       

		# 	Interest accrued in year
        interest_accrued_list =[round(x*y,5) for x,y in zip(self.beggining_debt_list,self.nominal_interest_rate_lc_list)]
        setattr(self, 'interest_accrued_list', self.clean_inf_array(interest_accrued_list))
		# 	Principal paid
		# 	Interest paid
        interest_paid_list =[round(x,5) for x in interest_accrued_list]
        setattr(self, 'interest_paid_list', interest_paid_list)

		# 	Total Loan Repayment
        total_loan_repayment_list =[x+y for x,y in zip(self.interest_accrued_list,self.principal_paid_list)]
        setattr(self, 'total_loan_repayment_list', total_loan_repayment_list)

		# 	Outstanding debt at end of year
        outstanding_debt_list= np.array(self.beggining_debt_list) + \
                              np.array(self.loan_disbursement_list) + \
                              np.array(self.interest_accrued_list) - \
                              np.array(self.total_loan_repayment_list) 
        setattr(self, 'outstanding_debt_list', self.clean_inf_array(outstanding_debt_list))	
        #print('outstanding_debt_list', outstanding_debt_list)
		# 	Debt cash Inflow in Local Currency
        debt_cash_inflow_lc_list=[x for x in self.loan_disbursement_list]
        setattr(self, 'debt_cash_inflow_lc_list', debt_cash_inflow_lc_list)

		# 	Total Loan Repayment as an outflow in Local Currency
        total_loan_repayment_ouflow_lc_list=[x for x in self.total_loan_repayment_list]
        setattr(self, 'total_loan_repayment_ouflow_lc_list', total_loan_repayment_ouflow_lc_list)
        #print('total_loan_repayment_ouflow_lc_list',total_loan_repayment_ouflow_lc_list)
        
        # 	Construction period flag
		# 	Operating period
		# 	Interest during Construction, Capitalized for Tax Purposes
        interest_during_construction_list= [x*y for x,y in zip(self.interest_accrued_list,self.construction_period_flag_list)]
        setattr(self, 'interest_during_construction_list', self.clean_inf_array(interest_during_construction_list))


       
        total_soft_capital_cost= np.sum(interest_during_construction_list)
        setattr(self, 'total_soft_capital_cost', total_soft_capital_cost)

        
        
        #Tax life of soft capital costs
        const_instalments= total_soft_capital_cost/self.tax_life_of_soft_capital_costs
        const_end= self.start_year + self.tax_life_of_soft_capital_costs-1
        soft_capital_cost_list= [const_instalments*x if (y>=self.start_year and y<=const_end) else 0 for x,y in zip(self.op_list,self.tp_list)]
        setattr(self, 'soft_capital_cost_list', soft_capital_cost_list)
       
        # 	Interest expense (for income statement)
        interest_expense_list= [x*y for x,y in zip(self.interest_accrued_list,self.op_list)]
        setattr(self, 'interest_expense_list', interest_expense_list)
       
       
    def _metric_depreciationForTaxPurposes(self):
        pass
       
    def _metric_finishedProdictEvaluationFIFO(self):
        # OPENING INVENTORY			
        #     Closing Inventory
        closing_inventory_list= [0 for x in self.tp_list]
        setattr(self, 'closing_inventory_list', closing_inventory_list)

        #     Quantity from previous year (closing inventory)
        qnty_prev_closing_inventory_list= list(self._accumulate_previous(self.closing_inventory_list))
        setattr(self, 'qnty_prev_closing_inventory_list', self.clean_inf_array(qnty_prev_closing_inventory_list))
        #     Unit cost from previous year per ton (nominal)
        
        # cost_of_opening_inventory_list =list(self._accumulate_previous(self.total_unit_cost_per_ton))
        # setattr(self, 'cost_of_opening_inventory_list', cost_of_opening_inventory_list)
        # #     Cost of opening inventory (using previous year's unit cost FIFO method)
        
        #Formuale =qnty_prev_closing_inventory_list*cost_of_opening_inventory_list
        cost_of_opening_inventory_list=[x*y for x,y in zip(self.qnty_prev_closing_inventory_list,
                                                             self.qnty_prev_closing_inventory_list )]
        setattr(self, 'cost_of_opening_inventory_list', self.clean_inf_array(cost_of_opening_inventory_list))           
        # ADDITIONS			
        #             Production Quantity
        #             Total unit cost of production per ton (nominal)
                    
        # WITHDRAWALS			
        #             Sales quantity
        #             Quantity sold from this yr's production
        qnty_sold_this_year_production_list=[x-y for x,y in zip(self.prod_qnty_list,self.qnty_prev_closing_inventory_list )]
        setattr(self, 'qnty_sold_this_year_production_list', self.clean_inf_array(qnty_sold_this_year_production_list))
        #             Cost of the proportion of sales produced in current year
        cost_of_proportional_sales=[x*y/1000 for x,y in zip(self.total_unit_cost_production_per_ton_list,
                                                             self.qnty_sold_this_year_production_list )]
        #             COST OF GOODS SOLD (FOR INCOME STATEMENT)
        cost_of_goods_sold_list =np.array(cost_of_opening_inventory_list) + np.array(self.clean_inf_array(cost_of_proportional_sales))
        setattr(self, 'cost_of_goods_sold_list', self.clean_inf_array(cost_of_goods_sold_list))           
                
        # CLOSING INVENTORY			
        #             Quantity remained (unsold) in year
        qnty_remained_unsold_list= self.qnty_prev_closing_inventory_list + \
                              np.array(self.prod_qnty_list) - \
                              np.array(self.sales_qnty_list) 
        setattr(self, 'qnty_remained_unsold_list', self.clean_inf_array(qnty_remained_unsold_list))      
        #             Cost of closing inventory (using current year's unit cost)
        cost_of_closing_inventory_list=np.array(self.total_unit_cost_production_per_ton_list) * \
                              np.array(self.qnty_remained_unsold_list)  
        setattr(self, 'cost_of_closing_inventory_list', self.clean_inf_array(cost_of_closing_inventory_list))

    

    def _metric_IncomeTaxStatement(self):
        #Nominal
       
        #1. Depreciation expense			
		# 	Operation period
		# 	Machinery depreciation expense
		# 	Buildings depreciation expense
		# 	Soft Capital Costs (Interest during construction)
        
		# 	Annual Depreciation Expense
        annual_dep_exp_list =np.array(self.depreciation_machinery_list) + \
                            np.array(self.depreciation_buildings_list) + \
                             np.array(self.soft_capital_cost_list) 
        setattr(self, 'annual_dep_exp_list', self.clean_inf_array(annual_dep_exp_list))

      

       
        #1. REVENUE
        #---------------------------------------------------------------
        #1.1 Net sales revenue

        #2. LESS OPERATING EXPENSES
        #---------------------------------------------------------------
        #   2.1 Cost of goods sold
                                                            
        #cost_of_goods_sold_list =1
        # Annual Depreciation Expense
        # Total Indirect Labour Cost
        # Cost of electricity (nominal)
        # Other Indirect Costs (nominal)
        #2.1 Total Operating Expenses
        total_operating_expenses_list= np.array(self.cost_of_goods_sold_list) + \
                                  np.array(self.annual_dep_exp_list)  + \
                                  np.array(self.cost_of_electricity_list) +  \
                                  np.array(self.other_indirect_costs_list) +  \
                                  np.array(self.total_indirect_labour_list)    
        
        setattr(self, 'total_operating_expenses_list', self.clean_inf_array(total_operating_expenses_list))

        #2.2 INCOME FROM OPERATIONS
        income_from_operations_list =np.array(self.net_sales_revenue_list)-np.array(self.total_operating_expenses_list)
        setattr(self, 'income_from_operations_list', self.clean_inf_array(income_from_operations_list))
        # Interest paid

        #2.3 PRE-TAX INCOME
        pre_tax_income_list= np.array(self.income_from_operations_list)- np.array(self.interest_expense_list)
        setattr(self, 'pre_tax_income_list', self.clean_inf_array(list(pre_tax_income_list)))
        # Cumulative losses
       
        cumulative_losses_list =list(self._accumulate_losess(self.pre_tax_income_list))
        setattr(self, 'cumulative_losses_list', self.clean_inf_array(cumulative_losses_list))
        # Taxable income (losses carried forward)
        taxable_income_list =list(self._accumulate_taxable_income(self.pre_tax_income_list,self.cumulative_losses_list))
        setattr(self, 'taxable_income_list', self.clean_inf_array(taxable_income_list))
        # Corporate income tax
        # Income tax payment
        income_tax_payment_list =[max(self.corporate_income_tax*x,0) for x in self.taxable_income_list]
        setattr(self, 'income_tax_payment_list', self.clean_inf_array(income_tax_payment_list))

        # NET AFTER-TAX INCOME
        next_after_tax_income_list =np.array(self.pre_tax_income_list)-np.array(self.income_tax_payment_list)
        setattr(self, 'next_after_tax_income_list', self.clean_inf_array(next_after_tax_income_list))
        #3. EQUITY
        # #----------------------------------------------------------------
       
  
    def _get_financial_npv(self, rate_, cashflows_in):
        """ 
        Excel assumes that the first value is at t=1 (no initial wealth), 
        while numpy-financial assumes the first value to be at t=0. 
        Therefore, In numpy you start with an initial wealth of 4000 and your result is 
        basically the excel result * 1.06. 

        It may be preferable to split the projected cashflow into an initial investment 
        and expected future cashflows. In this case, the value of the initial cashflow 
        is zero and the initial investment is later added to the future cashflows net present value:
        """
       
        cashflows= cashflows_in.copy()
        #cashflows=[round(i,1)  for i in  cashflows]
        initial_cashflow = cashflows[0]#.copy()
        cashflows[0] = 0
        # if abs(rate_-.12) <.001:
        #     print('-------------------------rateCF----------------------------')
        #     print(rate_,initial_cashflow, cashflows)
        npv_ =np.round(npf.npv(rate_, cashflows) + initial_cashflow, 1)
        return npv_
    def _get_loan_period_bounds(self):
        # loan bounds has flout with error from wtong user input correct here
        # or make sure user inputs correct values
        #print('reapymet: ' , self.loan_principal_repayment_flag_list)
        # get the first 1 index:
        i= self.loan_principal_repayment_flag_list.index(1)
        #after first pint 
        #----0 0 0 0 1 1 1 1 1 0 0 0 0
        j= self.loan_principal_repayment_flag_list.index(0,i)

        return i, j-1
                 
   
    
    def npv(self, cfList, r):
        sum_pv = 0  # <-- variable used to sum result
        for i, pmt in enumerate(cfList, start=1):  # <-- use of enumerate allows you to do away with the counter variables.
            sum_pv += pmt / ((1 + r) ** i)  # <-- add pv of one of the cash flows to the sum variable

        return sum_pv  # 

    def pv_gen(cfList, r):
        #An alternate implementation would be to yield individual PVs from a PV generator
        for i, pmt in enumerate(cfList, start=1):
            yield pmt / ((1 + r) ** i)

    def pv2(self, cfList, r):
        return (sum(self.pv_gen(cfList, r)))

   
    def _accumulate_investment_rollout_flag(self,list_):
        next_value =0
        for i in range(len(list_)):
            #if nothing and the is vale
            if self._sum_list(list_,0,i)==0 and list_[i]>0:
                next_value= 1
            else:
                next_value =0
            yield next_value

    def _sum_list(self, list_, i, j):
        sum_ =0
        for p in range (i,j):
            sum_ += list_[p]
        return sum_
    
   
    def _accumulate_harvesting(self,list_, operations_list):
        next_value =0
        for i in range(len(list_)):
            item = list_[i]
            next_value= self.clean_inf_array(next_value) + self.clean_inf_array(item)
            #if opertion has strted calcultea
            if sum(operations_list[:i+1])>0:
                yield next_value
            else:
                yield 0

    def _accumulate_addition(self,list_):
        next_value =0
        for item in list_:
            next_value= self.clean_inf_array(next_value) + self.clean_inf_array(item)
            yield next_value
    
    def _accumulate_difference(self,list_):
        next_value =0
        for item in list_:
            next_value= self.clean_inf_array(next_value) - self.clean_inf_array(item)
            yield next_value
    
    def _accumulate_previous(self,list_):
        next_value =0
        for i in range(len(list_)):
            if i>0:
                next_value= self.clean_inf_array(list_[i-1])
            else:
                next_value =0
            yield self.clean_inf_array(next_value)

    def _accumulate_beginning_debt(self,loan_disb_list, principal_paid_list):
        begin_debt= 0
        next_value=0
        for i in range(len(loan_disb_list)):
            outstanding_debt= begin_debt + loan_disb_list[i] - principal_paid_list[i]
            next_value=begin_debt
            #update
            begin_debt= outstanding_debt                 

            yield self.clean_inf_array(next_value)
    def _accumulate_nominal_interest_rate(self, inflation_rate_list, real_interest_rate,risk_premium):
        #i+r+(1+i+r)*x
        #c+(1+c)*x
        const_=real_interest_rate +risk_premium 
        for i in range(len(inflation_rate_list)):
            next_value= const_+(1+const_)*(inflation_rate_list[i]) 
            yield self.clean_inf_array(next_value)

    def _accumulate_nominal_interest_rate_lc(self, inflation_rate_list, discount_rate_equity):
        #i+r+(1+i+r)*x
        #c+(1+c)*x
        discount_rate_equity =round(discount_rate_equity,5)
        for i in range(len(inflation_rate_list)):
            next_value= discount_rate_equity+(1+discount_rate_equity)*(inflation_rate_list[i]) 
            yield self.clean_inf_array(next_value)
    def _accumulate_losess(self, pre_tax_income_list):
        next_value =0
        for i in range(len(pre_tax_income_list)):
            next_value= min((pre_tax_income_list[i] + next_value),0) 
            yield self.clean_inf_array(next_value)

    def _accumulate_taxable_income(self,pre_tax_income_list, cum_losses_list):
        next_value =0
        for i in range(len(pre_tax_income_list)):
            if i>0:
                next_value= max((pre_tax_income_list[i] + cum_losses_list[i-1]),0) 
            else:
                next_value= max(pre_tax_income_list[i], 0)
            yield self.clean_inf_array(next_value)

      
    def _accumulate_change_in(self,list_):
        next_value =0
        for i in range(len(list_)):
            if i>0:
                next_value= list_[i-1] - list_[i]
            else:
                next_value =-list_[i]
            yield self.clean_inf_array(next_value)
    def _accumulate_change_in_CB(self,list_):
        #next_value =0
        for i in range(len(list_)):
            if i>0:
                next_value= list_[i]-list_[i-1]
            else:
                next_value =list_[i]
            yield self.clean_inf_array(next_value)
           
    def _accumulate_price_index(self,list_,inflation_rate):
        next_value =1
        inflation_rate=round(inflation_rate,5)
        for i in range(len(list_)):
            if i >0:
                next_value= next_value*(inflation_rate+1)
            yield self.clean_inf_array(next_value)
    
    def _accumulate_salary_rate(self,list_,monthly_salary_rate, annual_incr):
        annual_incr =round(annual_incr,5)
        next_value =12*round(monthly_salary_rate,5)
        #print('Culprit:::',next_value,(1+annual_incr), round(next_value*(1+annual_incr),5))
        for i in range(len(list_)):
            if i >0:
                #use prev val
                if abs(next_value)<0.0001:
                    next_value=0
                if abs(annual_incr)<0.0001:
                    annual_incr=0
                next_value= round(next_value,5)*(1+annual_incr)
            yield self.clean_inf_array(round(next_value,5))

    def _accumulate_yearly_rate(self,list_,base_cost, annual_incr):
        next_value =base_cost
        annual_incr =round(annual_incr,5)
        for i in range(len(list_)):
            if i >0:
                #use prev val
                next_value= next_value*(1+annual_incr)
            yield self.clean_inf_array(next_value)
    def _accumulate_sales_qnty(self,list_, sales_qnty_list_):
        next_value=0
        i=int(0)
        k=int(0)
        for a,b in zip(list_, sales_qnty_list_):
            #print(i,k)
            if i > 0:
                next_value= list_[i-1] - list_[i]+ sales_qnty_list_[k]
            else:
                next_value=  sales_qnty_list_[k]- list_[i]
            i +=1
            k +=1
            yield self.clean_inf_array(next_value)


     
    def clean_inf_array(self,inputarray):
        #x[numpy.isneginf(x)] = 0
        if isinstance(inputarray,np.ndarray):
           new_x= np.nan_to_num(inputarray, neginf=0)
        elif isinstance(inputarray,list):
            new_x= np.nan_to_num(np.array(inputarray), neginf=0)
        elif isinstance(inputarray, int) or  isinstance(inputarray, float):
            #print(f'Main module:: {inputarray}==> {math.isinf(inputarray)}?? {np.isfinite(inputarray)}')
            #np.isfinite(x)
            if not np.isfinite(inputarray): #not math.isinf(float(inputarray)):
                new_x =0 
            else:
                new_x=inputarray
        else:
            #do nothing
            new_x=inputarray
        return new_x


    def __str__(self):
        """
        Print dictionary of object attributes but don't include the _initial_inputs dict.
        """
        return str({key: val for (key, val) in vars(self).items() if key[0] != '_'})
