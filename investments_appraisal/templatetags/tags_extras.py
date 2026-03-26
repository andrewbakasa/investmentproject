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

@register.simple_tag
def userIsOwnerAttrMethod(model, user):
    """
    Used for the 'Entrepreneur' span.
    Logic: Return 'hidden' or a specific style if the user isn't the owner.
    """
    if model.user == user:
        return "" # or whatever attribute makes it visible
    return "hidden"

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