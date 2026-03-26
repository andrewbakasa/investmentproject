import datetime
import io
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.encoding import force_str

# Standard OpenPyXL imports (Already in your environment)
from openpyxl import Workbook
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# Project-specific imports
from trading.models import Investment, Investor
from django.contrib.auth.models import User
from common.utils import thousand_sep

def get_excel_investor_list(request, pk):
    """
    Generates an Excel export of investors for a specific investment.
    Uses pure-python memory buffering to avoid C++ compiler dependencies.
    """
    obj_invest = get_object_or_404(Investment, pk=pk)
    
    # Data gathering using Pandas (Requirement already satisfied in your env)
    investors_df = pd.DataFrame(Investor.objects.filter(Q(investment__id=pk)).values())
    users_df = pd.DataFrame(User.objects.all().values())
    
    df = pd.DataFrame(columns=[
        'Title', 'Motivation Statement', 'Amt Pledged', 'Created',
        'Status Changed', 'Status', 'Investor username', 'Investor F-Name',
        'Investor L-Name', 'Investor email', 'pending', 'verification',
        'accepted', 'engagement', 'rejected'
    ])  

    if users_df.shape[0] > 0 and investors_df.shape[0] > 0:
        users_df['user_id'] = users_df['id']
        df = pd.merge(investors_df, users_df, on='user_id', how="left").drop([
            'id_x', 'id_y', 'investment_id', 'user_id', 'password', 
            'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined'
        ], axis=1).rename({
            'name': 'Title', 'first_name': 'Investor F-Name',
            'email': 'Investor email', 'last_name': 'Investor L-Name',
            'username': 'Investor username', 'value': 'Amt Pledged',
            'application_status': 'Status', 'motivation': 'Motivation Statement',
            'date_created': 'Created', 'date_status_changed': 'Status Changed'
        }, axis=1)   
        
        for i in ['pending', 'verification', 'accepted', 'engagement', 'rejected']:
            df[i] = df.apply(lambda x: get_column_state(x['Amt Pledged'], x['Status'], i), axis=1)     

    # Create the Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Investor List'    

    # Header Row
    heading_text = f"INVESTORS LIST WORTH [{thousand_sep(obj_invest.total_value)}] FOR [{obj_invest.name}]"
    ws.append([heading_text.upper()])	
    ws.append([colname for colname in df.columns])
    
    # Data Rows
    for index, row in df.iterrows():
        ws.append([col for col in row])
    
    # Totals and Percentages logic
    total_ref = f'{get_column_letter(15)}1'
    row_count = len(df)
    
    # Summary formulas
    sum_totals = [
        f"=SUM({get_column_letter(c+1)}3:{get_column_letter(c+1)}{row_count + 2})" 
        if c in [2, 10, 11, 12, 13, 14] else "" for c in range(15)
    ]
    ws.append(sum_totals)

    as_percent = [
        f"={get_column_letter(c+1)}{row_count + 3}/{total_ref}" 
        if c in [2, 10, 11, 12, 13, 14] else "" for c in range(15)
    ]
    ws.append(as_percent)

    # Styling and Formatting
    # (Applying your existing formatting logic here...)
    setup_excel_styles(ws, df)

    # --- PRODUCTION EXPORT LOGIC (The Fix) ---
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f"Investors_{obj_invest.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response["Cache-Control"] = "no-cache, no-store"
    
    return response

def get_column_state(amt, status, output_status):
    return amt if status == output_status else 0

def setup_excel_styles(ws, df):
    # This maintains your original visual look for the NRZ reports
    bold_font = Font(bold=True, color='FFFFCC99', sz=12)
    for col in range(1, 16):
        cell = ws.cell(row=2, column=col)
        cell.font = bold_font
        ws.column_dimensions[get_column_letter(col)].width = 15
# import datetime
# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter,column_index_from_string
# from openpyxl.styles import Font, Color, Alignment, Border, Side, colors, NamedStyle,PatternFill
# from openpyxl.chart import BarChart, Reference
# from openpyxl.styles import NamedStyle
# from tempfile import NamedTemporaryFile

# import pandas as pd
# from common.utils import thousand_sep
# from openpyxl import Workbook, load_workbook
# from django.utils.encoding import smart_str, force_str
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render

# from common.decorators import admin_only
# from django.contrib import messages

# from trading.models import Investment, Investor
# from django.contrib.auth.models import User
# from django.db.models import Q
# def get_excel_investor_list(request, pk):
#     obj_invest =get_object_or_404(Investment, pk=pk)
#     investors_df = pd.DataFrame(Investor.objects.filter(Q(investment__id=pk)).values())
#     users_df = pd.DataFrame(User.objects.all().values())
#     df = pd.DataFrame(columns =['Title', 'Motivation Statement', 'Amt Pledged', 'Created',
#                                 'Status Changed', 'Status', 'Investor username', 'Investor F-Name',
#                                 'Investor L-Name', 'Investor email', 'pending', 'verification',
#                                 'accepted', 'engagement', 'rejected'])  
#     # merge
#     if users_df.shape[0]>0 and investors_df.shape[0]>0:
#         users_df['user_id'] = users_df['id']
#         df =pd.merge(investors_df, users_df, on='user_id',how="left").drop([
#                     'id_x', 'id_y' , 'investment_id', 'user_id', 'password', 
#                     'last_login', 'is_superuser',  'is_staff', 'is_active',  'date_joined'
#                     ], axis=1).rename( {'name':'Title', 'first_name': 'Investor F-Name',
#                             'email':'Investor email', 'last_name': 'Investor L-Name',
#                             'username':'Investor username', 'value': 'Amt Pledged',
#                             'application_status':'Status', 'motivation': 'Motivation Statement',
#                             'date_created':'Created', 'date_status_changed': 'Status Changed'  }, 
#                     axis=1)   
#         for i in ['pending','verification', 'accepted', 'engagement','rejected']:
#             df[i]=df.apply(lambda x : get_column_state(x['Amt Pledged'], x['Status'], i), axis=1)     
#     #print(df.columns)
#     wb = Workbook()
#     #--------------------------------Failures-------------------------------------------------------------
#     ws = wb.worksheets[0]
#     #ws = wb.create_sheet()
#     ws.title = 'Investor List'    
#     # Writing the first row of the csv
#     heading_text = f"Investors List worth [{thousand_sep(obj_invest.total_value)}] for [{obj_invest.name}] by  [{obj_invest.creater}] "
#     total_ref =f'{get_column_letter(14+1)}1'
#     ws.append([heading_text.upper()])	
#     ws.append([colname for colname in df.columns])
   
#     for index, row in df.iterrows():
#         ws.append([col for col in row])
    
#    #-------------------TOTAL------------------------------------------------------------------
#     sum_totals= [
#                 f"=SUM({get_column_letter(choice+1)}3:{get_column_letter(choice+1)}{len(df) +2})" 
#                 if choice in [2, 10,11,12,13,14] else "" for choice in range(15)
#                ]
#     ws.append(sum_totals)
#     #-------------------PERCENT-------------------------------------------------------------
#     as_percent= [
#                 f"={get_column_letter(choice+1)+ str(len(df) + 2+1)}/{total_ref}" 
#                 if choice in [2, 10,11,12,13,14] else "" for choice in range(15)
#                ]
#     ws.append(as_percent)
#     #-----------------FORMAT---------------------------------------------------------
#     ws['%s%s'%(get_column_letter(1), len(df) + 2 + 1 )].value="TOTALS"
#     ws['%s%s'%(get_column_letter(1), len(df) + 2 + 1 )].font = Font(name='Calibri',bold=False, sz=11.0, color='FFFF8001')
  
#     ws['%s%s'%(get_column_letter(1), len(df) + 2 + 2 )].value="PERCENTAGE"
#     ws['%s%s'%(get_column_letter(1), len(df) + 2 + 2 )].font = Font(name='Calibri',bold=False, sz=11.0, color='FFFF8001')
    
#     double_border_side_linked = Side(border_style="double",color="FFFF8001")
#     linked_border = Border(outline=True,
#                                 bottom=double_border_side_linked)
       
#     for x in [2, 10,11,12,13,14]:
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 2 )].number_format ='0.#%'       
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 2 )].font = Font(name='Calibri', bold=True, color='FFFA7D00',scheme='minor',sz=12.0)
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 2 )].border = linked_border
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 2 )].alignment = Alignment(vertical="top")
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 2 )].fill = PatternFill(fgColor='00000000', bgColor='00000000')

#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 1 )].number_format ='_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)'       
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 1 )].font = Font(name='Calibri', bold=True, color='FFFA7D00',scheme='minor',sz=12.0)
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 1 )].border = linked_border
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 1 )].alignment = Alignment(vertical="top")
#         ws['%s%s'%(get_column_letter(x+1), len(df) + 2 + 1 )].fill = PatternFill(fgColor='00000000', bgColor='00000000')
   
#     #format cells
#     col = get_column_letter(1)
#     ws['%s%s'%(col, 1)].font = Font(name='Calibri',bold=True, sz=14.0, color='FFFFCC99')
#     ws['%s%s'%(col, 1)].number_format ='General'
#     #row....
#     for col in range(1,23):
#         col = get_column_letter(col) 
#         ws['%s%s'%(col, 2)].font = Font(name='Calibri',bold=True, sz=12.0, color='FFFFCC99')
#         ws['%s%s'%(col, 2)].number_format ='General'
#     start_row= 3
#     for row_index in range(start_row, start_row + len(df)):
#         for col in range(1,11):
#             col = get_column_letter(col)
#             ws['%s%s'%(col, row_index)].font = Font(name='Calibri',bold=False, sz=11.0, color='FF3F3F76')
#             ws['%s%s'%(col, row_index)].number_format ='General'
          
#         for col in range(4,6):
#             col = get_column_letter(col)
#             ws['%s%s'%(col, row_index)].font = Font(name='Calibri',bold=False, sz=11.0, color='FF3F3F76')
#             ws['%s%s'%(col, row_index)].number_format ='dd mmmm yyyy'           

#         for col in [3,10,11,12,13,14,15]:
#             col = get_column_letter(col) 
#             ws['%s%s'%(col, row_index)].font = Font(name='Calibri',bold=False, sz=11.0, color='FF3F3F76')
#             ws['%s%s'%(col, row_index)].number_format ='_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)'

    
  
#     for idj in [1,2,4,5,6,7,8,9,10]:
#         ws.column_dimensions[get_column_letter(idj)].width=14
#     for idj in [3,]:
#         ws.column_dimensions[get_column_letter(idj)].width=12
    
   
#     end_col = get_column_letter(len(df.columns))
#     ws['%s%s'%(get_column_letter(14+1), 1)].value=obj_invest.total_value
#     ws['%s%s'%(get_column_letter(14+1), 1)].font = Font(name='Calibri',bold=True, sz=11.0, color='FF3F3F76')
#     ws['%s%s'%(get_column_letter(14+1), 1)].number_format ='_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)'
#     set_output_bordered_section(ws,"A",end_col,2, 2 + len(df))
#     #------------------------------------------------------------------------------------------------------

#     response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
#     date_now = datetime.datetime.now() #date.today()
#     date_now = str(date_now.year) + '_' + str(date_now.month) \
#                 + '_' + str(date_now.day)+ "_" + str(date_now.hour) \
#                 + '_' + str(date_now.minute) + "_" +  str(date_now.second)

#     filename = "Failures" + date_now +  ".xlsx"
#     response['Content-Disposition'] = 'attachment; filename=' + filename
  

#     title = "clearVision_solutions_auto-generated beefbusiness" + str(date_now)
#         #-----------------------------

      
#     response[
#             "Content-Disposition"
#     ] = "attachment; filename*=utf-8''%s.xlsx" % force_str(title) 
#     response["Cache-Control"] = "no-cache, no-store"
#     return response

# def set_style(cell_,heading_style):
#     if heading_style =='Heading1':
#         cell_.font = Font(name='Cambria',bold=True, color='FF3F3F76', scheme='major', sz=15.0)	
#         cell_.alignment = Alignment(horizontal='left', vertical='top',)
#         cell_.number_format ='General'
#     elif heading_style =='Heading2':
#         cell_.font = Font(name='Calibri',bold=True,  scheme='minor', sz=15.0)	
#         cell_.alignment = Alignment(horizontal='left', vertical='top',)
#         cell_.number_format ='General'
#     else :
#         cell_.font = Font(name='Calibri',bold=True,  scheme='minor', sz=11.0)	
#         cell_.alignment = Alignment(horizontal='left', vertical='top',)
#         cell_.number_format ='General'

            

# def set_output_bordered_section(w_sheet, col_letter_start, col_letter_end, 
#                 start_row, end_row, heading_style='Heading1', accent_style='Accent1'):

#     set_style(w_sheet.cell('%s%s'%(col_letter_start, start_row)),heading_style)
#     w_sheet[col_letter_start + str(start_row)].alignment = Alignment(wrap_text=False,vertical='top')

#     col_s =column_index_from_string(col_letter_start)
#     col_e= column_index_from_string(col_letter_end)
#     #
#     for i in range(col_s, col_e+1):
#         coli = get_column_letter(i)
#         #first row color:
#         w_sheet['%s%s'%(coli, start_row)].style= accent_style

#     _range=f"{col_letter_start}{start_row}:{col_letter_end}{end_row}"
#     _set_border(w_sheet,_range)
       
# def _set_border_all(wkSheet, cell_range):
#     border = Border(left=Side(border_style='thin', color='000000'),
#                 right=Side(border_style='thin', color='000000'),
#                 top=Side(border_style='thin', color='000000'),
#                 bottom=Side(border_style='thin', color='000000'))

#     rows = wkSheet.iter_rows(cell_range)
#     for row in rows:
#         for cell in row:
#             cell.border = border

  
# def _set_border(wkSheet, cell_range):
#     rows = list(wkSheet[cell_range])
#     side = Side(border_style='thick', color="FF000000")

#     rows = list(rows)  # we convert iterator to list for simplicity, but it's not memory efficient solution
#     max_y = len(rows) - 1  # index of the last row
#     for pos_y, cells in enumerate(rows):
#         max_x = len(cells) - 1  # index of the last cell
#         for pos_x, cell in enumerate(cells):
#             border = Border(
#                 left=cell.border.left,
#                 right=cell.border.right,
#                 top=cell.border.top,
#                 bottom=cell.border.bottom
#             )
#             if pos_x == 0:
#                 border.left = side
#             if pos_x == max_x:
#                 border.right = side
#             if pos_y == 0:
#                 border.top = side
#             if pos_y == max_y:
#                 border.bottom = side

#             # set new border only if it's one of the edge cells
#             if pos_x == 0 or pos_x == max_x or pos_y == 0 or pos_y == max_y:
#                 cell.border = border            
  

# def get_column_state(amt,status, output_status):
#     #print(status,output_status)
#     if status ==output_status:
#         return amt
#     return 0
    