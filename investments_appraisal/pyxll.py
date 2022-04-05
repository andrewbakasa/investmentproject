""" 
PyXLL is currently the only package that enables developers to write fully featured 
Excel addins in Python. It embeds the Python interpreter into Excel so that it can 
be used as a complete VBA replacement. You can think of it conceptually as 
being similar to something like Excel-DNA for C#, except that it is dynamic 
and imports your Python code while Excel is running – so there’s no add-in to 
build and no need to restart Excel when modifying your Python code. 
"""

# PyXLL has a config file (pyxll.cfg) which contains a list of all the modules 
# that will be imported when Excel starts. By adding the module above to the 
# list in that file, PyXLL will expose the ‘py_test’ 
# function to Excel as a user defined function to be called from a worksheet.


# Using PyXLL, you can write Python code to create:

# Worksheet functions (user defined functions, called from Excel worksheet formulas)
# Macros
# Menus
# Custom Ribbon Bars
# Real Time Data feeds
# Writing a user defined function with PyXLL requires the ‘xl_func’ decorator to be applied to a normal Python function:

from pyxll import xl_func
 
@xl_func
def py_test(a, b, c):
    return (a + b) * c


from pyxll import xl_macro, xl_app


@xl_macro
def macro1():
    xl = xl_app()

    # 'xl' is an instance of the Excel.Application object

    # Get the current ActiveSheet (same as in VBA)
    sheet = xl.ActiveSheet

    # Call the 'Range' method on the Sheet
    xl_range = sheet.Range('B11:K11')

    # Call the 'Select' method on the Range.
    # Note the parentheses which are not required in VBA but are in Python.
    xl_range.Select()   



# Default Color Index as per 18.8.27 of ECMA Part 4
COLOR_INDEX = (
    '00000000', '00FFFFFF', '00FF0000', '0000FF00', '000000FF', #0-4
    '00FFFF00', '00FF00FF', '0000FFFF', '00000000', '00FFFFFF', #5-9
    '00FF0000', '0000FF00', '000000FF', '00FFFF00', '00FF00FF', #10-14
    '0000FFFF', '00800000', '00008000', '00000080', '00808000', #15-19
    '00800080', '00008080', '00C0C0C0', '00808080', '009999FF', #20-24
    '00993366', '00FFFFCC', '00CCFFFF', '00660066', '00FF8080', #25-29
    '000066CC', '00CCCCFF', '00000080', '00FF00FF', '00FFFF00', #30-34
    '0000FFFF', '00800080', '00800000', '00008080', '000000FF', #35-39
    '0000CCFF', '00CCFFFF', '00CCFFCC', '00FFFF99', '0099CCFF', #40-44
    '00FF99CC', '00CC99FF', '00FFCC99', '003366FF', '0033CCCC', #45-49
    '0099CC00', '00FFCC00', '00FF9900', '00FF6600', '00666699', #50-54
    '00969696', '00003366', '00339966', '00003300', '00333300', #55-59
    '00993300', '00993366', '00333399', '00333333',  #60-63
) 
   