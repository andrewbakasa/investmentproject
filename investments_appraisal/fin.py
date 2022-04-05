import numpy as np
import scipy.optimize as optimize
from scipy.optimize import fsolve

def npv2_(cf, rate=0.1, print_dcf=False):
    if len(cf) >= 2:
        dcf = [x * (1 /((1 + rate) ** (i))) for i,x in enumerate(cf)]
        if print_dcf:
            print(f'DCF: {dcf}')
       
        return sum(dcf)
    elif len(cf) == 1:
        return cf[0]
    else:
        return 0

def irr2_(cf,guess=[0]):
    
    cf = np.array(cf)
    if (np.where(cf <0,1,0).sum() ==0) | (np.where(cf>0,1,0).sum() == 0):
        #if the cashflows are all positive or all negative, no point letting the algorithm
        #search forever for a solution which doesn't exist
        return np.nan
    guess_list = np.array(guess) 
    
    f = lambda x: npv2_(cf,x)    
    answer_list= fsolve(f,guess_list)
    unique_= np.unique([round(x,5) for x in answer_list])
    
    return unique_[np.argmax(unique_)]
def irr2(cf):
    f = lambda x: npv2_(cf, rate=x)
    r = optimize.root(f, [0])
    return r

