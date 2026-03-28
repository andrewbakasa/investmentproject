from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

# --- NEW INVESTOR TAGS ---
@register.simple_tag
def userhasNewInvestorsMethod(user):
    return False 

@register.simple_tag
def userNewInvestorsCountMethod(user):
    return 0

# --- ACCEPTED INVESTOR TAGS ---
@register.simple_tag
def useracceptedAsInvestorMethod(user):
    return False

@register.simple_tag
def useracceptedInvestmentsCountMethod(user):
    """Returns the count of investments already approved for the user."""
    return 0

# --- STAFF/ADMIN TAGS ---
@register.simple_tag
def userisStaffMethod(user):
    return user.is_staff if user.is_authenticated else False

# --- GENERAL UTILITY ---
@register.simple_tag
def userhasNotifications(user):
    """Commonly used in this template for the bell icon."""
    return False

@register.simple_tag
def userInvestorMethod(model, user):
    """
    Used in the class attribute of the project div.
    Return a string (CSS class) or empty string.
    """
    # Logic: Check if the user is an investor in this specific model
    return "" 


# --- MISSING TAGS FOR INVESTMENT DETAILS ---

@register.simple_tag
def UserIsInvestorStatement(model, user):
    """Returns a string describing the user's relationship to the investment."""
    if not user or not user.is_authenticated:
        return 'I am NOT an Investor'
    return model.userIsInvestorStatement(user)

@register.simple_tag
def userInvestorEngagedMethod(model, user):
    """Checks if the user has an 'engagement' status."""
    if not user or not user.is_authenticated:
        return False
    # Using your model's related set
    return model.investor_set.filter(user=user, application_status="engagement").exists()

@register.simple_tag
def userInvestorRejectedMethod(model, user):
    """Checks if the user is rejected or if the investment is closed."""
    if not user or not user.is_authenticated:
        return False
    
    # Check if rejected status exists
    is_rejected = model.investor_set.filter(user=user, application_status="rejected").exists()
    
    # Check if investment is closed (prevents editing/new actions)
    is_closed = getattr(model, 'closed_status', False)
    
    return is_rejected or is_closed
@register.simple_tag
def userIsOwnerAttrMethod(model, user):
    # Use 'creater' as defined in your model
    if hasattr(model, 'creater') and model.creater == user:
        return "" 
    return "hidden"

@register.simple_tag
def UserIsInvestorStake(model, user):
    """
    Calls the logic defined in the Investment model 
    to get the percentage stake.
    """
    if not user or not user.is_authenticated:
        return 0
    # This calls the method you just showed me in the model
    return model.userIsInvestorStake(user)



@register.simple_tag
def userInvestorValueMethod(model, user):
    """Used in the data-invest-value attribute."""
    return 0

@register.simple_tag
def userInvestorPercentMethod(model, user):
    """Used for the counter text next to the cut icon."""
    return "0%"


@register.filter
def shrink_num(value):
    """
    Converts a large integer into a friendly text representation (k, M, B).
    Example: 1500 -> 1.5k
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return value


    """
    Checks if the user has an active stake in the current model/investment.
    Returns True/False or a specific value based on your requirements.
    """
    if not user or not user.is_authenticated:
        return False
    
    # You can customize this logic later to check your Investment/Trade models
    # For now, we return False to stop the crash and keep the page loading.
    return False