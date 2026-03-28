import numpy as np
import warnings
from scipy.optimize import brentq

def npv2_(cf, rate=0.1):
    """
    Calculates NPV using vectorized numpy operations.
    Suppresses runtime warnings for division by zero or invalid values 
    often encountered during sensitivity analysis.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        
        cf = np.asarray(cf)
        if cf.size == 0:
            return 0.0
        
        periods = np.arange(len(cf))
        # This is where the 'divide by zero' usually happens if rate is -1
        return np.sum(cf / (1 + rate)**periods)

def irr2_(cf):
    """
    Calculates IRR using Brent's method with suppressed warnings.
    """
    cf = np.asarray(cf)
    
    # 1. Sign check: IRR requires at least one inflow and one outflow
    if not (np.any(cf < 0) and np.any(cf > 0)):
        return np.nan

    f = lambda r: npv2_(cf, rate=r)

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        try:
            # Search bracket from -99.9% to 10,000%
            return brentq(f, -0.999, 100.0)
        except (ValueError, RuntimeError):
            return np.nan

def get_investment_metrics(cf, discount_rate=0.1):
    """
    High-level helper for AJAX views.
    """
    try:
        npv_val = npv2_(cf, rate=discount_rate)
        irr_val = irr2_(cf)
        
        return {
            "npv": round(float(npv_val), 2),
            "irr": round(float(irr_val), 4) if not np.isnan(irr_val) else None,
            "status": "success"
        }
    except Exception as e:
        # Standard exceptions still get caught here for debugging
        return {"status": "error", "message": str(e)}
# import numpy as np
# from scipy.optimize import brentq

# def npv2_(cf, rate=0.1):
#     """
#     Calculates NPV using vectorized numpy operations for speed.
#     """
#     cf = np.asarray(cf)
#     if cf.size == 0:
#         return 0.0
    
#     # Create an array of powers: [0, 1, 2, ..., n]
#     periods = np.arange(len(cf))
#     # NPV = sum( CF / (1 + r)^t )
#     return np.sum(cf / (1 + rate)**periods)

# def irr2_(cf):
#     """
#     Calculates IRR using Brent's method. 
#     Brentq is faster and more stable than fsolve for 1D root finding.
#     """
#     cf = np.asarray(cf)
    
#     # 1. Quick check for valid Cash Flow signs
#     # An IRR only exists if there is at least one negative and one positive value.
#     if not (np.any(cf < 0) and np.any(cf > 0)):
#         return np.nan

#     # 2. Define the objective function: NPV(r) = 0
#     f = lambda r: npv2_(cf, rate=r)

#     try:
#         # 3. Use brentq with a defined bracket to avoid -100% (division by zero)
#         # We search between -0.999 (-99.9%) and 100.0 (10,000%)
#         # This prevents the "iteration not making progress" error.
#         return brentq(f, -0.999, 100.0)
#     except (ValueError, RuntimeError):
#         # Fallback if no root is found in the bracket
#         return np.nan

# def get_investment_metrics(cf, discount_rate=0.1):
#     """
#     Helper for your AJAX view to get all metrics at once safely.
#     """
#     try:
#         npv_val = npv2_(cf, rate=discount_rate)
#         irr_val = irr2_(cf)
        
#         return {
#             "npv": round(float(npv_val), 2),
#             "irr": round(float(irr_val), 4) if not np.isnan(irr_val) else None,
#             "status": "success"
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
# import numpy as np
# import scipy.optimize as optimize
# from scipy.optimize import fsolve

# def npv2_(cf, rate=0.1, print_dcf=False):
#     if len(cf) >= 2:
#         dcf = [x * (1 /((1 + rate) ** (i))) for i,x in enumerate(cf)]
#         if print_dcf:
#             print(f'DCF: {dcf}')
       
#         return sum(dcf)
#     elif len(cf) == 1:
#         return cf[0]
#     else:
#         return 0

# def irr2_(cf,guess=[0]):
    
#     cf = np.array(cf)
#     if (np.where(cf <0,1,0).sum() ==0) | (np.where(cf>0,1,0).sum() == 0):
#         #if the cashflows are all positive or all negative, no point letting the algorithm
#         #search forever for a solution which doesn't exist
#         return np.nan
#     guess_list = np.array(guess) 
    
#     f = lambda x: npv2_(cf,x)    
#     answer_list= fsolve(f,guess_list)
#     unique_= np.unique([round(x,5) for x in answer_list])
    
#     return unique_[np.argmax(unique_)]
# def irr2(cf):
#     f = lambda x: npv2_(cf, rate=x)
#     r = optimize.root(f, [0])
#     return r

