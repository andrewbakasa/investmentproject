from multiprocessing import Pool
import multiprocessing
import os
import time
import numpy as np
import pandas as pd
from sklearn.model_selection._search import ParameterGrid
#from sklearn.model_selection._search import ParameterGrid
import copy
from tqdm import tqdm

from scipy import stats
import numpy as np

# If 'rand' was being used in the code below, 
# we define it here using the modern NumPy equivalent
#rand = np.random.rand

from concurrent.futures import ProcessPoolExecutor, as_completed
import math
const_ =0.0001
# stats.norm.ppf(q=100,loc=1,scale=1.2)
# stats.norm.cdf()
class BookstoreModel():
    def __init__(self, unit_cost=0, selling_price=0, unit_refund=0, 
                 order_quantity=0, demand=0):
        self.unit_cost = unit_cost
        self.selling_price = selling_price
        self.unit_refund = unit_refund
        self.order_quantity = order_quantity
        self.demand = demand
        
    def update(self, param_dict):
        """
        Update parameter values
        """
        for key in param_dict:
            setattr(self, key, param_dict[key])
        
    def order_cost(self):
        return self.unit_cost * self.order_quantity
    
    def sales_revenue(self):
        return np.minimum(self.order_quantity, self.demand) * self.selling_price
    
    def refund_revenue(self):
        return np.maximum(0, self.order_quantity - self.demand) * self.unit_refund
    
    def total_revenue(self):
        return self.sales_revenue() + self.refund_revenue()
    
    def refund_revenue(self):
        return np.maximum(0, self.order_quantity - self.demand)
    
    def profit(self):
        '''
        Compute profit in bookstore model
        '''
        profit = self.sales_revenue() + self.refund_revenue() - self.order_cost()
        return profit
       
    def __str__(self):
        """
        Print dictionary of object attributes but don't include the _initial_inputs dict.
        """
        return str({key: val for (key, val) in vars(self).items() if key[0] != '_'})
        
def parallel_data_table(model, scenario_inputs, outputs):
    # Clone the model
    model_clone = copy.deepcopy(model)
    dt_param_grid = list(ParameterGrid(scenario_inputs))
    # Scenario loop
    args = []
    for i in tqdm(range(len(dt_param_grid))):
       args.append({'model_clone': model_clone,  'outputs': outputs,   'params': dt_param_grid[i]})
    cpu_no = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_no) 

    future_res = pool.map(data_table_sample, args)
    if not isinstance(future_res,list):
        dictionary_list = [f for f in future_res.get()]
    else:
        dictionary_list = [f for f in future_res]

    df_final = pd.DataFrame.from_dict(dictionary_list)
    return df_final


def data_table_sample(args):
    model_clone = args['model_clone']
    outputs = args['outputs']
    params = args['params']
    model_clone.update(params)
    # Create a result dictionary based on a copy of the scenario inputs
    result = copy.copy(params)
    # Loop over the list of requested outputs
    for output in outputs:
        # Compute the output.
        out_val = getattr(model_clone, output)()
        # Add the output to the result dictionary
        #result[output] = out_val
        if isinstance(out_val, dict):
            for key, val in out_val.items():
                result[key] = val
        else:
            result[output] = out_val     
   
    return result    

def data_table(model, scenario_inputs, outputs):
    '''Create n-inputs by m-outputs data table. 

    Parameters
    ----------
    model : object
        User defined object containing the appropriate methods and properties for computing outputs from inputs
    scenario_inputs : dict of str to sequence
        Keys are input variable names and values are sequence of values for each scenario for this variable.
        
        Is consumed by scikit-learn ParameterGrid() function. See https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ParameterGrid.html
    outputs : list of str
        List of output variable names

    Returns
    -------
    results_df : pandas DataFrame
        Contains values of all outputs for every combination of scenario inputs
    '''
    
    # Clone the model using deepcopy
    model_clone = copy.deepcopy(model)
    
    # Create parameter grid
    dt_param_grid = list(ParameterGrid(scenario_inputs))
    
    # Create the table as a list of dictionaries
    results = []

    # Loop over the scenarios
    for params in dt_param_grid:
        # Update the model clone with scenario specific values
        model_clone.update(params)
        # Create a result dictionary based on a copy of the scenario inputs
        result = copy.copy(params)
        # Loop over the list of requested outputs
        for output in outputs:
            # Compute the output.
            out_val = getattr(model_clone, output)()
            # Add the output to the result dictionary
            #result[output] = out_val
            if isinstance(out_val, dict):
                for key, val in out_val.items():
                    result[key] = val
            else:
                result[output] = out_val 
        
        # Append the result dictionary to the results list
        results.append(result)

    # Convert the results list (of dictionaries) to a pandas DataFrame and return it
    results_df = pd.DataFrame(results)
    
    return results_df
        

def goal_seek(model, obj_fn, target, by_changing, a, b, N=100):
    '''Approximate solution of f(x)=0 on interval [a,b] by bisection method.

    Parameters
    ----------
    model : object
        User defined object containing the appropriate methods and properties for doing the desired goal seek
    obj_fn : function
        The function for which we are trying to approximate a solution f(x)=target.
    target : float
        The goal
    by_changing : string
        Name of the input variable in model
    a,b : numbers
        The interval in which to search for a solution. The function returns
        None if (f(a) - target) * (f(b) - target) >= 0 since a solution is not guaranteed.
    N : (positive) integer
        The number of iterations to implement.

    Returns
    -------
    x_N : number
        The midpoint of the Nth interval computed by the bisection method. The
        initial interval [a_0,b_0] is given by [a,b]. If f(m_n) - target == 0 for some
        midpoint m_n = (a_n + b_n)/2, then the function returns this solution.
        If all signs of values f(a_n), f(b_n) and f(m_n) are the same at any
        iteration, the bisection method fails and return None.
    '''
    # TODO: Checking of inputs and outputs
    
    # Clone the model
    model_clone = copy.deepcopy(model)
    
    # The following bisection search is a direct adaptation of
    # https://www.math.ubc.ca/~pwalls/math-python/roots-optimization/bisection/
    # The changes include needing to use an object method instead of a global function
    # and the inclusion of a non-zero target value.
    
    setattr(model_clone, by_changing, a)
    f_a_0 = getattr(model_clone, obj_fn)()
    setattr(model_clone, by_changing, b)
    f_b_0 = getattr(model_clone, obj_fn)()
    
    if (f_a_0 - target) * (f_b_0 - target) >= 0:
        # print("Bisection method fails.")
        return None
    
    # Initialize the end points
    a_n = a
    b_n = b
    for n in range(1, N+1):
        # Compute the midpoint
        m_n = (a_n + b_n)/2
        
        # Function value at midpoint
        setattr(model_clone, by_changing, m_n)
        f_m_n = getattr(model_clone, obj_fn)()
        
        # Function value at a_n
        setattr(model_clone, by_changing, a_n)
        f_a_n = getattr(model_clone, obj_fn)()
        
        # Function value at b_n
        setattr(model_clone, by_changing, b_n)
        f_b_n = getattr(model_clone, obj_fn)()

        # Figure out which half the root is in, or if we hit it exactly, or if the search failed
        if (f_a_n - target) * (f_m_n - target) < 0:
            a_n = a_n
            b_n = m_n
        elif (f_b_n - target) * (f_m_n - target) < 0:
            a_n = m_n
            b_n = b_n
        elif f_m_n == target:
            #print("Found exact solution.")
            return m_n
        else:
            #print("Bisection method fails.")
            return None
    
    # If we get here we hit iteration limit, return best solution found so far
    return (a_n + b_n)/2

    
def simulate(model, random_inputs, outputs, scenario_inputs=None, keep_random_inputs=False):
    '''Simulate model for one or more scenarios

    Parameters
    ----------
    model : object
        User defined object containing the appropriate methods and properties for computing outputs from inputs
    random_intputs : dict of str to sequence of random variates
        Keys are stochastic input variable names and values are sequence of $n$ random variates, where $n$ is the number of simulation replications
    outputs : list of str
        List of output variable names
    scenario_inputs : optional (default is None), dict of str to sequence
        Keys are deterministic input variable names and values are sequence of values for each scenario for this variable. Is consumed by
        scikit-learn ParameterGrid() function. See https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ParameterGrid.html
    keep_random_inputs : optional (default is False), boolean
        If True, all the random input variates are included in the results dataframe

    Returns
    -------
    results_df : pandas DataFrame
        Values of all outputs for each simulation replication. If `scenario_inputs` is not None, then this is also for every combination of scenario inputs
    '''
    
    # Clone the model
    model_clone = copy.deepcopy(model)
    
    # Update clone with random_inputs
    #print('Rando Inputs>>>>>........................inside monteCarlo>>>')
    if not random_inputs==None: # or random_inputs.empty:
        model_clone.update(random_inputs)
    
    # Store raw simulation input values if desired
    if keep_random_inputs:
        scenario_base_vals = vars(model_clone)
    else:
        scenario_base_vals = vars(model)
    

  

    # Initialize output counters and containers
    scenario_num = 0
    scenario_results = []
    
    # Check if multiple scenarios
    if scenario_inputs is not None:
        # Create parameter grid for scenario inputs
        sim_param_grid = list(ParameterGrid(scenario_inputs))
        # Scenario loop
        #for params in sim_param_grid:

        for i in tqdm(range(len(sim_param_grid))):
           
            #sleep 1 sec to avoid comupter freese
            #time.sleep(0.2)
            #model_clone.update(params)
            model_clone.update(sim_param_grid[i])
            # Initialize scenario related outputs
            result = {}
            
            scenario_vals = copy.copy(sim_param_grid[i])
            """  producing error bacuase of dictionaries"""
            result['scenario_base_vals'] = scenario_base_vals
            result['scenario_num'] = scenario_num
            result['scenario_vals'] = scenario_vals
            raw_output = {}
            
            # Output measure loop
            for output_name in outputs:
                output_array = getattr(model_clone, output_name)()
                if isinstance(output_array, dict):
                    for key, val in output_array.items():
                        raw_output[key] = val
                    # or
                    # raw_output=output_array
                else:
                   raw_output[output_name] = output_array 
            
            #item_workshop.extend(item_mpd)
            """ 
            d = {'abc': 'abc', 'def': {'ghi': 'ghi', 'jkl': 'jkl'}}
            for element in d.values():
                if isinstance(element, dict):
                for k, v in element.items():
                    print(k,' ',v)
            """
            # Gather results for this scenario
            result['output'] = raw_output
            scenario_results.append(result)
            scenario_num += 1
        #print('Completed Simulation')        
        return scenario_results

    else:
        # Similar logic to above, but only a single scenario
        results = []
        result = {}
        """  producing error bacuase of dictionaries"""
        result['scenario_base_vals'] = scenario_base_vals
        result['scenario_num'] = scenario_num
        result['scenario_vals'] = {}
        
        raw_output = {}
       
        # Output measure loop
        for output_name in outputs:
            output_array = getattr(model_clone, output_name)()
            if isinstance(output_array, dict):
                for key, val in output_array.items():
                    raw_output[key] = val
                # or
                # raw_output=output_array
            else:
                raw_output[output_name] = output_array 
    
       
       
        result['output'] = raw_output  
        results.append(result)

        return results

def parallel_simulation(request, model, random_inputs, outputs, scenario_inputs=None, total_runs=10000,keep_random_inputs=False):
    
    #request.session['count']=0
     # Clone the model
    model_clone = copy.deepcopy(model)
    if not random_inputs==None: # or random_inputs.empty:
        model_clone.update(random_inputs)
    
    # Store raw simulation input values if desired
    if keep_random_inputs:
        scenario_base_vals = vars(model_clone)
    else:
        scenario_base_vals = vars(model)
    
    request.session['count']=0
    request.session['total_runs']=total_runs
    request.session.save()
    #print('state of affars>>>>>>>>', request.session['count'])
    #sim_param_grid = list(ParameterGrid(scenario_inputs))

    # Scenario loop
    #for params in sim_param_grid:
    args = []
    for i in tqdm(range(total_runs)):
       #i =int(rand()* len(sim_param_grid))
        #sim_param_grid=[]
        sim_param={}
        for item in scenario_inputs.keys():           
            pos=int(len(scenario_inputs[item])* rand())
            sim_param[item]= scenario_inputs[item][pos] 
        
        args.append({'scenario_inputs': scenario_inputs, 'model_clone': model_clone, 
                     'scenario_base_vals': scenario_base_vals, 'outputs': outputs, 
                     'sim_param': sim_param, 'scenario_num': i })
    
   
    cpu_no = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_no)  
   
    #n=len(sim_param_grid) 
    """ 
    #working but no progess bar
    future_res = pool.map_async(simulation_sample, args)
    # for _ in tqdm(pool.map_async(simulation_sample, args), total=len(total_runs)):
    #     print(_)
    if not isinstance(future_res,list):
        res = [f for f in future_res.get()]
    else:
        res = [f for f in future_res]
   
    
    """
    res =[] 
    #future_res =pool.imap(simulation_sample, args)
    for i in tqdm(pool.imap(simulation_sample, args), total=total_runs):
        request.session['count']+=1
        res.append(i)
        request.session.save()
        #print('here...........', request.session['count'])
      
    # #This is goood
    # with Pool(processes=cpu_no-1) as pool:
    #     #progress_bar = tqdm(total=total_runs)
    #     #imap_unordered        
    #     future_res = tqdm(pool.imap(simulation_sample, args), total=total_runs)
    #     tqdm()
    #     # fetch the lazy results
    #     if not isinstance(future_res,list):
    #         res = [f for f in future_res]
    #     else:
    #         res = [f for f in future_res]
   
    """   
    with ProcessPoolExecutor(max_workers=cpu_no) as executor:
        # total argument for tqdm is just the number of submitted tasks:
        with tqdm(total=n) as progress_bar:
            futures = {}
            for idx, dt in enumerate(args):
                arg= args[idx]
                future = executor.submit(simulation_sample, dt)
                futures[future] = idx
            results = [None] * len(args) # pre_allocate slots
            for future in as_completed(futures):
                idx = futures[future] # order of submission
                results[idx] = future.result()
                progress_bar.update(1) # advance by 1
        res = [ent for sublist in results for ent in sublist]
        #data = pd.DataFrame(data, columns = cols)
     """
    
    
    """ 

    with Pool(cpu_no) as p, tqdm(total=n) as pbar:
        res1 = [p.apply_async(
            simulation_sample, args=(i,), callback=lambda _: pbar.update(i)) for i in range(n)]
        print(i, "......................", res1)
        #res = [r.get() for r in res1]
        print(list(res1))
        if not isinstance(res1,list):
            res = [f for f in res1.get()]
        else:
            res = [f.get() for f in res1]
    """
    # with mp.Pool(processes=cpu_no) as pool:
    #      future_res = list(tqdm(pool.map_async(simulation_sample, args)))
    # res = [f.get() for f in future_res]
    # print(res[0])
   
    return res

def simulation_sample(args):
    scenario_inputs = args['scenario_inputs']
    model_clone = args['model_clone']
    scenario_base_vals = args['scenario_base_vals']
    scenario_num = args['scenario_num']
    outputs = args['outputs']
    sim_param = args['sim_param']
    #request_ = args['request']
    #sleep 1 sec to avoid comupter freese
    time.sleep(0.01)
    
    #------add
    #request.session['count']= request.session['count'] + 1
    #print('parallelelelelelele>>>>>>>>', request.session['count'])
    
     # Check if multiple scenarios
    if scenario_inputs is not None:
       
        model_clone.update(sim_param)
        # Initialize scenario related outputs
        result = {}
       
        scenario_vals = copy.copy(sim_param)
        
        result['scenario_base_vals'] = scenario_base_vals
        result['scenario_num'] = scenario_num
        result['scenario_vals'] = scenario_vals
        raw_output = {}
        
        # Output measure loop
        for output_name in outputs:
            output_array = getattr(model_clone, output_name)()
            if isinstance(output_array, dict):
                for key, val in output_array.items():
                    raw_output[key] = val
            else:
                raw_output[output_name] = output_array 
        
           
        # Gather results for this scenario
        result['output'] = raw_output
    else:
        # Similar logic to above, but only a single scenario
        result = {}
        result['scenario_base_vals'] = scenario_base_vals
        result['scenario_num'] = scenario_num
        result['scenario_vals'] = {}
        
        raw_output = {}
    
        for output_name in outputs:
            output_array = getattr(model_clone, output_name)()
            if isinstance(output_array, dict):
                for key, val in output_array.items():
                    raw_output[key] = val
            else:
                raw_output[output_name] = output_array
       
        result['output'] = raw_output 
    return result
   


def senstivity_table_sample(args):
    dt_param_ranges_1 = args['dt_param_ranges_1']
    model_clone = args['model_clone'] 
    dict_of_para_clone = args['dict_of_para_clone'] 
    inparameter = args['inparameter']   
    outputs = ['_model_datatable_outputs_dict']
    
    #each process has its own model object
    model_clone = copy.deepcopy(model_clone)

    sens_df = data_table(model_clone, dt_param_ranges_1, outputs)
    #print(dt_param_ranges_1)
    #print('Columns:',sens_df.columns)

    #---get value that makes npv zero
    x_npv_0, simulation_results_1 =get_x_npv_zero(sens_df,inparameter,model_clone)
    included=-1
    #add new row if it doesnt exist lready
    mask_new_insert =abs(sens_df[inparameter]-x_npv_0)<=const_ 
    if sens_df[mask_new_insert].empty:
        # #print(f'in parralel sensitivity table, new npv zero found {inparameter}  @ {x_npv_0}')
        # new_dt_param_ranges_1 = {inparameter: np.array([round(x_npv_0,5)])}
        # new_sens_df = data_table(model_clone, new_dt_param_ranges_1, outputs)
        # #before_len =len(sens_df)
        #print(simulation_results_1)
        sens_df2= pd.concat([sens_df,simulation_results_1],  ignore_index=True)
        #print('len be4 and after: ' , before_len, len(sens_df2))
        sens_df= sens_df2.copy()
        sens_df.sort_values(by=[inparameter],inplace=True) 
        #print(sens_df)
        included=1
        
    # sort by ascending 
    sens_df.sort_values(by=[inparameter],inplace=True) 
    #------------round
    sens_df['npv']=sens_df['npv'].apply(lambda x: round(x,5))
    dict_ = {}
    dict_['inparameter']=inparameter
    dict_['x_npv_0']=round(x_npv_0,5)
    dict_['included']=included
    
    dict_['df']=sens_df
    #model_clone.
    dict_['params']=dict_of_para_clone#dt_param_ranges_1

    # if 'equity' in inparameter:
    #     print(f'val: {x_npv_0}')
        #print(dict_)

    return dict_

# def modified(args,    model, para_name, para_val_list):

#     dt_param_ranges_1 = args['dt_param_ranges_1']
#     model_clone = args['model_clone'] 
#     para_name = args['inparameter']   
#     outputs = ['_model_datatable_outputs_dict']
#     para_val_list= args['list']
   
#     #each process has its own model object
#     model_clone = copy.deepcopy(model_clone)
    

#     dt_param_ranges_1 = {para_name: np.array(para_val_list)}   
#     #retun metric cal with canges
#     outputs = ['_model_outputs_dict']

#     dt_param_ranges_1 = {para_name: np.array(para_val_list)}   
#     #retun metric cal with canges
#     outputs = ['_model_outputs_dict']

#     # Use data_table function to create 1-way data table
#     simulation_results_1 = data_table(model, dt_param_ranges_1, outputs)  



#     input_x=simulation_results_1[para_name].tolist()
#     outpuy_y=simulation_results_1['npv'].tolist()
#     grad_av= gradient(outpuy_y , input_x)
#     #-----Y= ax +b
#     # X Intercept ===Y=0
#     #b=-ax
#     #gradient* x
#     #b=                   Y    -a*     x
#     b_intercept= outpuy_y[0]- grad_av*input_x[0]
#     return  round(grad_av,10),round(b_intercept,10)

def sim_sensitivity(args):
    model_clone= args['model_clone']
    name= args['name']
    values= args['list']
    grad_, b_intercept,initial_point= get_sensitivity_grad(model_clone, name, values)
    x_npv_0 =-b_intercept/grad_ if float(abs(grad_)) >= float(const_) else 0

   
    if float(abs(grad_)) >= float(const_) :#and  not ('annual'  in name):
        inputx =[x_npv_0]
        x_npv_0, _ =aproximate_zero_npv(model_clone, name, grad_,inputx,initial_point) 

    v={'parameter':name , 'gradient': round(grad_,10), 'abs_grad': round(abs(grad_),10), 'x_npv_0':round(x_npv_0,5) }
   
    return v

def aproximate_zero_npv(model, para_name, ave_grad,para_value, initial_point):    
    simulation_results_1 =None
    #initiate
    next_para_value=para_value
    next_x =para_value[0]
    initial_learning_rate =0.001
    
    flag_once=False
    input_x=[]
    input_x.append(initial_point['x'])
    output_y=[]
    output_y.append(initial_point['y'])
   
    change_in_x=0
    check_direction =[]
    for i in range(200): 
        #dynamic
        #1.... x=0.89712, npv=-2751  next val:-22.10
        #2......x=-22.210 npv=3600,0000000 a big num
        # !. learning rate should be very slow    
        npv_x, simulation_results_1 = get_npv(model, para_name, next_para_value)
        # if 'discount' in para_name:
        #     print(npv_x)
        #     print(simulation_results_1)
       
        if isinstance(npv_x,list):
            npv_x=npv_x[0]
            output_y.append(npv_x)
            input_x.append(next_para_value[0])
            #-------101010-----------------
            
            check_direction.append(1 if npv_x >=0 else 0)
       
         
        #get here once only    
        if flag_once==False:
            flag_once=True 
            #were are close to answer
            initial_learning_rate =0.001#min(0.1 *abs(ave_grad/npv_x), .1)

        learning_rate=step_decay(i,initial_learning_rate)
      
        #x2    =   x1               - @Y1/gradient   
        #-22.10   =0.89712          - @(-2751/-119)
        #learnig rate proptional to gradient
        """   
        x[t] = x[t-1] – 𝜂∇f(x[t-1]) + 𝛼*Δx[t-1]
        where Δx[t-1] represents the change in x, i.e.,

        Δx[t] = x[t] – x[t-1]

        The initial change at t=0 is a zero vector. For this problem Δx[0] = (0,0).

        Adding Momentum
        Gradient descent can run into problems such as:

        Oscillate between two or more points
        Get trapped in a local minimum
        Overshoot and miss the minimum point
        To take care of the above problems, a momentum term can be added to the update equation of gradient descent algorithm as:

        """
        if len(output_y)>=2: 
            current_grad= gradient(np.array(output_y[-2:]), np.array(input_x[-2:]))
        else:
            current_grad= 0#ave_grad

        #if gradient is nan
        if current_grad!=current_grad:
            current_grad=0
            next_x=clean_inf_array(next_x)
            return  round(next_x,5), simulation_results_1

      
        #next_x = next_para_value[0] -max(abs(learning_rate*current_grad),abs(next_para_value[0])) + 0.1*change_in_x
 
       
        next_x = next_para_value[0] -(npv_x/current_grad if current_grad!=0 else 0)#+ 0.1*change_in_x
        #change_in_x = next_x - next_para_value[0]
        """ 
        if 'discount' in para_name:
            print(f'{i}.output{output_y[-2:]} input {input_x[-2:]} grad: {current_grad} lr:{learning_rate} {para_name}: ave_grad: {ave_grad}, npv:{npv_x}, prev_val: {next_para_value[0]} ,ext_val: {next_x}')

        """
        
        if abs(npv_x)<.1:
            next_x=clean_inf_array(next_x)
            return  round(next_x,5), simulation_results_1
            
        #loop
        next_para_value=[round(next_x,5)]

    next_x=clean_inf_array(next_x)
    return round(next_x,5), simulation_results_1

def step_decay(epoch, initial_lrate=.1):
   #initial_lrate = 0.1
   drop = 0.5
   epochs_drop = 10.0
   lrate = initial_lrate * math.pow(drop,  
           math.floor((1+epoch)/epochs_drop))
   return lrate
def clean_inf_array(inputarray):
    #x[numpy.isneginf(x)] = 0
    if isinstance(inputarray,np.ndarray):
        new_x= np.nan_to_num(inputarray, neginf=0)
    elif isinstance(inputarray,list):
        new_x= np.nan_to_num(np.array(inputarray), neginf=0)
    elif isinstance(inputarray, int) or  isinstance(inputarray, float):
        #print(f'what if module :: {inputarray}==> {math.isinf(inputarray)}?? {np.isfinite(inputarray)}')
        #np.isfinite(x)
        if not np.isfinite(inputarray): #not math.isinf(float(inputarray)):
            new_x =0 
        else:
            new_x=inputarray
    else:  #do nothing
        new_x=inputarray
    return new_x

def get_npv(model, para_name, para_val_list):
    
    dt_param_ranges_1 = {para_name: np.array(para_val_list)}   
    #retun metric cal with ranges
    outputs = ['_model_outputs_dict']

    # Use data_table function to create 1-way data table
    simulation_results_1 = data_table(model, dt_param_ranges_1, outputs) 
    simulation_results_1['npv']=simulation_results_1['npv'].apply(lambda x: round(x,5))
   
    input_x=simulation_results_1[para_name].tolist()
    outpuy_y=simulation_results_1['npv'].tolist()
    return  outpuy_y,simulation_results_1
def get_sensitivity_grad(model, para_name, para_val_list):
    
    dt_param_ranges_1 = {para_name: np.array(para_val_list)}   
    #retun metric cal with canges
    outputs = ['_model_outputs_dict']

    # Use data_table function to create 1-way data table
    simulation_results_1 = data_table(model, dt_param_ranges_1, outputs)  
    input_x=simulation_results_1[para_name].tolist()
    outpuy_y=simulation_results_1['npv'].tolist()
    grad_av= gradient(outpuy_y , input_x)

    closest_point= np.argmin(np.abs(np.array(outpuy_y)))
    initial_point= {'x':input_x[closest_point], 'y': outpuy_y[closest_point]}
    #-----Y= ax +b
    # X Intercept ===Y=0
    #b=-ax
    #gradient* x
    #b=                   Y    -a*     x
    b_intercept= outpuy_y[0]- grad_av*input_x[0]
    return  round(grad_av,10),round(b_intercept,10),initial_point
def get_x_npv_zero(dfin, para_name,model_clone):
    df= dfin.copy()
    input_x=df[para_name].tolist()
    outpuy_y=df['npv'].tolist()
    grad_av= gradient(outpuy_y , input_x)
    #-----Y= ax +b
    # X Intercept ===Y=0
    #b=-ax
    #gradient* x
    #b=                   Y    -a*     x
    simulation_results_1 = None
    b_intercept= outpuy_y[0]- grad_av*input_x[0] 

    closest_point= np.argmin(np.abs(np.array(outpuy_y)))
    initial_point= {'x':input_x[closest_point], 'y': outpuy_y[closest_point]}
    x_npv_0 =-b_intercept/grad_av if abs(float(grad_av)) >= float(const_) else 0
    if abs(grad_av) >= const_ :#and  not ('annual'  in para_name) :
        inputx =[round(x_npv_0,5)]
        x_npv_0, simulation_results_1 =aproximate_zero_npv(model_clone, para_name, grad_av, inputx,initial_point)
    """ 
    if 'discount' in para_name:
        #print(f'check???? {grad_av} {const_}', abs(grad_av) >= const_, not ('annual'  in para_name))
        print(f" Output>>>> {para_name} : {x_npv_0}")
        # trim val 
    """
    if abs(x_npv_0) < const_:
        x_npv_0=0
    return round(x_npv_0,5), simulation_results_1

def gradient(outpuy_y , input_x):
    """ 
    f = np.array([1, 2, 4, 7, 11, 16], dtype=float)
    np.gradient(f)
    #array([1. , 1.5, 2.5, 3.5, 4.5, 5. ])
    
    np.gradient(f, 2)
    #array([0.5 ,  0.75,  1.25,  1.75,  2.25,  2.5 ])

    # Spacing can be also specified with an array that represents the coordinates
    # of the values F along the dimensions.
    # For instance a uniform spacing:

    x = np.arange(f.size)
    np.gradient(f, x)
    #array([1. ,  1.5,  2.5,  3.5,  4.5,  5. ])

    #Or a non uniform one:

    x = np.array([0., 1., 1.5, 3.5, 4., 6.], dtype=float)
    grad= np.gradient(f, x) 
    #array([1. ,  3. ,  3.5,  6.7,  6.9,  2.5])
    """
    y= np.array(outpuy_y, dtype=float)
    x= np.array(input_x, dtype=float)
    grad=  np.gradient(y, x)

    #remove np.na()
    grad = grad[~np.isnan(grad)]  
    av_gradient=round(np.average(grad),10)

    #print('check granding? ', grad, 'average:' , av_gradient)
 
    return av_gradient

def get_para_data_table_sensitivity(model, para_, para_values):
    dt_param_ranges_1 = {para_: para_values}   
    outputs = ['_model_datatable_outputs_dict']
    
    sens_df = data_table(model, dt_param_ranges_1, outputs)
    # print('in senstivity>>>>>>>>>>>')
    # print(sens_df.columns)
    # print(sens_df)
    sens_df.sort_values(by=[para_],inplace=True) 
    x_npv_0,simulation_results_1  =get_x_npv_zero(sens_df,para_,model) 
    return sens_df, round(x_npv_0,5)
def get_sensitivity_gradient(model,input_x):
    # Clone the model
    model_clone = copy.deepcopy(model)
    
   
    cpu_no = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_no)   
    args = []
    for i in tqdm(range(len(input_x))):
       args.append({'model_clone': model_clone, 'name': input_x[i]['name'], 
                     'list':input_x[i]['list']})
    
   
    future_res = pool.map_async(sim_sensitivity, args)
    dictionary_list = [f for f in future_res.get()]    
    
    df_final = pd.DataFrame.from_dict(dictionary_list)
    results_df= df_final.sort_values(by=['abs_grad'],ascending=False)
    #print('Gradient........................')  
    #print(results_df)  
    return results_df
def get_data_table_sensitivity_in_parrallel(model, input_list,dict_of_para):
    #any diff
     
    model_clone = copy.deepcopy(model)
    dict_of_para_clone = copy.deepcopy(dict_of_para)
    outputs = ['_model_datatable_outputs_dict']
    args = []
    for i in tqdm(range(len(input_list))):
       args.append({'model_clone': model_clone,  'outputs': outputs, 'inparameter':input_list[i]['name'],
                    'dt_param_ranges_1' :{input_list[i]['name']: input_list[i]['list']},
                    'dict_of_para_clone':dict_of_para_clone
                    })   
     
    #print('args', args)
    cpu_no = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_no) 

    future_res = pool.map_async(senstivity_table_sample, args)
    if not isinstance(future_res,list):
        dictionary_list = [f for f in future_res.get()]
    else:
        dictionary_list = [f for f in future_res]

    new_dict_of_dict= {}
    for i in dictionary_list:
        key_ =i['inparameter']
        dict_={}
        #this diff doesnt have added list.....
        dict_['df']=i['df'].sort_values(by=[key_])
        #update this to reflect added row here under
        dict_['x_npv_0']=i['x_npv_0']

        dict_['included']=i['included']
        dict_['params']=i['params']
    
        new_dict_of_dict[key_]= dict_
       
    #print(new_dict_of_dict)
    #k={
    # 'price':{'df':df, 'params'....}
    # 'survival_rate':{'df':df, 'params'....}
    # }
    
    return new_dict_of_dict


def get_data_table_sensitivity_in_single_file(model, input_list):
     
    model_clone = copy.deepcopy(model)
    outputs = ['_model_datatable_outputs_dict']
    dictionary_list = []
    args={}
    for i in tqdm(range(len(input_list))):
        args={'model_clone': model_clone,  'outputs': outputs, 'inparameter':input_list[i]['name'],
                    'dt_param_ranges_1' :{input_list[i]['name']: input_list[i]['list']}}
        dict_= senstivity_table_sample(args)
        dictionary_list.append(dict_)
    
    new_dict_of_dict= {}
    for i in dictionary_list:
        key_ =i['inparameter']
        dict_={}
        #this diff doesnt have added list.....
        dict_['df']=i['df'].sort_values(by=[key_])
        #update this to reflect added row here under
        dict_['x_npv_0']=i['x_npv_0']

        dict_['included']=i['included']
       
    
    
        new_dict_of_dict[key_]= dict_
       
   
    
    return new_dict_of_dict
def get_data_table(model):
    dt_param_ranges_1 = {'initial_pens_employed': np.arange(1, 100, 9)}
    dt_param_ranges_1 = {'initial_pens_employed': np.array([1,10,50])}
    # 2-way table
    dt_param_ranges_2 = {'initial_pens_employed': np.array([1,10,50,500,1000]),
                    'discount_rate_equity': np.array([.1,.12,.15])}

    # n-way table
    dt_param_ranges_n = {'initial_pens_employed': np.array([1,10,50,500]),
                        'cattle_survival_rate': np.array([.9,.95,1]),
                    'discount_rate_equity': np.array([.1,.12,.15])}
 
    #retun metric cal with changes
    outputs = ['_model_datatable_outputs_dict']

    
    simulation_results_1 = parallel_data_table(model, dt_param_ranges_n, outputs)
    simulation_results_1.sort_values(by=['npv'],ascending=False,inplace=True)  
    return simulation_results_1


   
def monteCarlo_sim(request, model,npv_bin_size, num_reps = 10, 
                  total_runs=10000, selected_inputs_dict=None,total_params=None):
    # print('............selected_inputs_dict..............................')
    # print(selected_inputs_dict)
    """
    1. selected_inputs_dict:
    Has a list, in order of decraesing grad, of all parameter with a gradient (sensitive)

    2. base_scenario_inputs:
    Brings in item defined with probability of occurence
    
    3. Calcultate interference: [1 INTERSECTION 2]
    """
    if hasattr(model,'base_scenario_inputs'):
        base_scenario_inputs=model.base_scenario_inputs
    else:
        #if not yet set , set it now
        model._set_parameters_simulation(num_reps)
        base_scenario_inputs=model.base_scenario_inputs

    from numpy.random import default_rng
    rg = default_rng(4470)
    from scipy.stats import norm
   #0
    sim_outputs = ['_model_outputs_dict']
 
    #-----input with highest gradient selected first
    scenario_inputs={}

    if not selected_inputs_dict==None:
        scenario_inputs={}
        limit_vars = 0
        #---limit to 5 variables
        if total_params ==None:
            limit_vars= len(selected_inputs_dict)
        else:
            limit_vars = total_params
        
        for item in selected_inputs_dict[:limit_vars]:
            if  item in base_scenario_inputs.keys():
                #already defined.... stats
                scenario_inputs[item]=base_scenario_inputs[item]
            else:
                
                if hasattr(model, item):
                    input_var = getattr(model, item)
                    scenario_inputs[item]=rg.normal(input_var,get_alternative_sd(input_var,3,.3), num_reps)
                    
                else:
                    scenario_inputs[item]=rg.normal(0,get_alternative_sd(0,3,.3), num_reps)
        
    else:
        #get only top four items
        keys_= []
        for i in base_scenario_inputs.keys():
            keys_.append(i)

        selected_keys = keys_[:4] 
        scenario_inputs={}
        for item in selected_keys:
            scenario_inputs[item]=base_scenario_inputs[item]  

    #-----------------------------------------------------------------------------------------
    
    random_inputs =None
    model_results = parallel_simulation(request, model, random_inputs, sim_outputs,  scenario_inputs,total_runs)
    model2_results_df = get_sim_results_df(model_results)
    
    #-------------save data---------------    
    workpath = get_path()
    file_name= os.path.join(workpath, 'data/temp_data.csv')   
    model2_results_df.to_csv(file_name, index = False, header=True)
    #--------------------------------------------------

    npv_series= model2_results_df['npv']
    #print(model2_results_df)
    #print('Probability NPV==0: >>>>', stats.percentileofscore(npv_series, 0) / 100.0)
    min_index =npv_series.argmin()
    max_index =npv_series.argmax()

 

    cols= model2_results_df.columns.tolist()
    arrmin= []
    arrmax= []
    for item_name in cols:
        l1={}
        item_val =model2_results_df.iloc[min_index][item_name]
        l1['name']=item_name
        l1['val']=item_val
        arrmin.append(l1)

        item_val =model2_results_df.iloc[max_index][item_name]
        l2={}
        l2['name']=item_name
        l2['val']=item_val
        arrmax.append(l2)
    min_values='   Min Values:>>>> {'
    for i in arrmin:
        min_values += f"  {i['name']} : @ {i['val']},"
    min_values+='}'
    max_values='    Max Values:>>>>> {'
    for i in arrmax:
        max_values += f"  {i['name']} : @ {i['val']}, "
    max_values+='}'
    #print('Min NPV:', npv_series.min(),'Max NPV:', npv_series.max(),  min_values, max_values)
    # print('Used Inputs...........')
    # print(scenario_inputs.keys())
    return  cumfreq(model2_results_df,npv_bin_size), np.sort(np.array(npv_series.tolist())), scenario_inputs



def cumfreq(df,bins=100):
    range_ = int(df['npv'].max())-int(df['npv'].min())
    lower_= int(df['npv'].min())
    upper_= int(df['npv'].max())            
    step =int(range_/bins)
   
    cdf =[round(stats.percentileofscore(df['npv'], y) / 100.0,3) for y in range(lower_,upper_+step, step)]
    y =[round(probability_npv(df,y-step,y),3) for y in range(lower_,upper_+step, step)]
    #y =list(_accumulate_pos_difference(cdf))
    x = lower_ + np.linspace(0, bins * step,  step)
    x =[y  for y in range(lower_,upper_+step, step)]

    prob_npv_zero= probability_atleast(df, 0)
    mean= stats.describe(df['npv']).mean
    variance= stats.describe(df['npv']).variance
    # print('older mu:', mean)
    # print('older variance:', variance)
    
    _, mean= _get_variance(df['npv'].tolist())

    return {'x':x, 'y':y,'cdf':cdf ,'prob_npv_zero':prob_npv_zero, 
            'mean' : mean, 'variance' : variance }#,bins,lower_, upper_
  
def probability_upto(df, x):
    return probability_npv(df, None, x)

def probability_atleast(df, x):
    return probability_npv(df,x)


def probability_npv(df, x=None, y=None):
    # Probability profit is between x-----y
    if x==None and y==None:
        val = 0
    elif x==None:
        #--------y no lower bound
        val=stats.percentileofscore(df['npv'], y) / 100.0
    elif y==None:
        #x----------no upper bound
        val= 1- stats.percentileofscore(df['npv'], x) / 100.0
    else:
        #x------y inbetween
        val=(stats.percentileofscore(df['npv'], y) - stats.percentileofscore(df['npv'], x)) / 100.0
   
    return val
def _get_variance(list_):
    arr= np.array(list_)
    mu= np.mean(arr)
    _ = None
    #print('mu', mu)
    #print(arr)
    # diff1= arr-mu
    # diff2= arr-mu
    # var=diff1*diff2/len(list_-1)
    # print('var', var)
    return _ ,mu

  
def _accumulate_pos_difference(list_):
    next_value =0
    for item in list_:
        next_value= item -next_value 
        yield next_value
def get_alternative_sd(ds_mean, ds_sd_percent, new_sd):
    if ds_mean==0:
        return  abs(new_sd)
    else:
        return ds_mean*(1 + abs(ds_sd_percent))

def get_path():
    return os.path.dirname(os.path.abspath(__file__)) #Returns the Path your .py file is in
def get_sim_results_df(results):
    
    dictionary_list = []    
    #for r in results:
    for i in tqdm(range(len(results))):
      
        r= results[i]      
        dictionary_data ={}
        for key, val in r['output'].items():
            dictionary_data[key] = val
        dictionary_data['scenario_num'] = r['scenario_num']
        for key, val in r['scenario_vals'].items():
            dictionary_data[key] = val
        # for key, val in r['scenario_base_vals'].items():
        #     dictionary_data[key] = val
        dictionary_list.append(dictionary_data)

    # results_df = pd.concat(dfs)
    df_final = pd.DataFrame.from_dict(dictionary_list)
 
    return df_final