import numpy as np
import warnings

def npv2_(cf, rate=0.1):
    """Calculates NPV using vectorized numpy operations."""
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        cf = np.asarray(cf)
        if cf.size == 0:
            return 0.0
        periods = np.arange(len(cf))
        return np.sum(cf / (1 + rate)**periods)

def irr2_(cf, tol=1e-6, max_iter=100):
    """
    Calculates IRR using the Bisection Method (replaces scipy.optimize.brentq).
    """
    cf = np.asarray(cf)
    if not (np.any(cf < 0) and np.any(cf > 0)):
        return np.nan

    # Define the search bracket
    low = -0.999
    high = 100.0
    
    # Check if a solution exists in the bracket
    if npv2_(cf, low) * npv2_(cf, high) > 0:
        return np.nan

    for _ in range(max_iter):
        mid = (low + high) / 2
        val = npv2_(cf, mid)
        if abs(val) < tol:
            return mid
        if npv2_(cf, low) * val < 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2

def get_investment_metrics(cf, discount_rate=0.1):
    try:
        npv_val = npv2_(cf, rate=discount_rate)
        irr_val = irr2_(cf)
        return {
            "npv": round(float(npv_val), 2),
            "irr": round(float(irr_val), 4) if not np.isnan(irr_val) else None,
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
# import numpy as np
# import warnings
# from scipy.optimize import brentq

# def npv2_(cf, rate=0.1):
#     """
#     Calculates NPV using vectorized numpy operations.
#     Suppresses runtime warnings for division by zero or invalid values 
#     often encountered during sensitivity analysis.
#     """
#     with warnings.catch_warnings():
#         warnings.filterwarnings('ignore', category=RuntimeWarning)
        
#         cf = np.asarray(cf)
#         if cf.size == 0:
#             return 0.0
        
#         periods = np.arange(len(cf))
#         # This is where the 'divide by zero' usually happens if rate is -1
#         return np.sum(cf / (1 + rate)**periods)

# def irr2_(cf):
#     """
#     Calculates IRR using Brent's method with suppressed warnings.
#     """
#     cf = np.asarray(cf)
    
#     # 1. Sign check: IRR requires at least one inflow and one outflow
#     if not (np.any(cf < 0) and np.any(cf > 0)):
#         return np.nan

#     f = lambda r: npv2_(cf, rate=r)

#     with warnings.catch_warnings():
#         warnings.filterwarnings('ignore', category=RuntimeWarning)
#         try:
#             # Search bracket from -99.9% to 10,000%
#             return brentq(f, -0.999, 100.0)
#         except (ValueError, RuntimeError):
#             return np.nan

# def get_investment_metrics(cf, discount_rate=0.1):
#     """
#     High-level helper for AJAX views.
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
#         # Standard exceptions still get caught here for debugging
#         return {"status": "error", "message": str(e)}