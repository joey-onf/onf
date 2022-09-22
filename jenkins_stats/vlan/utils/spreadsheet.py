# -*- python -*-
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
""" . """

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pdb
import pprint

from pathlib import PurePath, Path

from openpyxl import Workbook

from openpyxl.cell import Cell
from openpyxl.worksheet.hyperlink import Hyperlink, HyperlinkList

# from openpyxl.worksheet.cell_range import CellRange

from openpyxl.styles import Alignment
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors

from openpyxl.styles import Font

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def init():
    pass

    # Register named styles: separate format from cells
    # https://openpyxl.readthedocs.io/en/stable/styles.html#creating-a-named-style

    # See also: merge styles

    # Conditional formatting
    # https://openpyxl.readthedocs.io/en/stable/formatting.html#conditional-formatting

    # Color if cell within range
    # https://openpyxl.readthedocs.io/en/stable/formatting.html
    # ws.conditional_formatting.add\
    #    (
    #        'D2:D10',
    #        CellIsRule(operator='between', formula=['1','5'], stopIfTrue=True, fill=redFill)
    #    )

    # Format using a formula
    # ws.conditional_formatting.add('E1:E10',
    #     FormulaRule(formula=['ISBLANK(E1)'], stopIfTrue=True, fill=redFill))

    # Row format
    # >>> red_fill = PatternFill(bgColor="FFC7CE")
    # >>> dxf = DifferentialStyle(fill=red_fill)
    # >>> r = Rule(type="expression", dxf=dxf, stopIfTrue=True)
    # >>> r.formula = ['$A2="Microsoft"']
    # >>> ws.conditional_formatting.add("A1:C10", r)
    #    =IF(A12>30, TRUE())
    #    0 == MOD(cell, 2)


    # worksheet.get_highest_row()
    # worksheet.get_highest_column()

    # TOTALS:  =SUM(range)

## -----------------------------------------------------------------------
## Todo: Refactor and move into a constants module
## -----------------------------------------------------------------------
def get_states():
    return['SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED']

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_aligns():
    orients = ['left', 'center', 'right']

    align = { orient : Alignment(horizontal=orient,vertical='center') for orient in orients }
    return align

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_fills():
    redFill = PatternFill(fill_type='solid', start_color='00FF0000')
    darkOrchidFill = PatternFill(fill_type='solid', start_color='9932CC')
    # purpleFill = PatternFill(fill_type='solid', start_color='C694F8')
    # purpleFill = PatternFill(fill_type='solid', start_color='AE7CE0') # light
    purpleFill = PatternFill(fill_type='solid', start_color='5F2D91')
    # purpleFill = PatternFill(fill_type='solid', start_color='9664C8')
    # https://hexcolorcodes.org/hex-code/9664c8    

    fill=\
        {
            'dark_orchid' : PatternFill(fill_type='solid', start_color='9932CC'),
            'purple' : PatternFill(fill_type='solid', start_color='5F2D91'),
            'red'    : PatternFill(fill_type='solid', start_color='00FF0000'),
        }

    
    # gradient = PatternFill(fill_type=None,
    # start_color='FFFFFFFF',
    # end_color='FF000000')    

    return fill

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_fonts() -> dict:

    color=\
        {
            'orange'  : 'FFBB00',
            'yellow'  : 'FAFA00',
            'yellow1' : 'FAFA00',
            'yellow2' : 'FFFF48',
        }

    fonts=\
        {
            color : Font(size=10, underline='single', color=hex_code, bold=True, italic=True)
            for color,hex_code in color.items()
        }

    return fonts

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
## changelog
    
#    font_color = styles.Color('00FF0000')
#    font = styles.Font(bold=True, color=font_color)
#    side = styles.Side(style=styles.borders.BORDER_THIN)
#    border = styles.Border(top=side, right=side, bottom=side, left=side)
#    alignment = styles.Alignment(horizontal='center', vertical='top')
#    fill_color = styles.Color(rgb='006666FF', tint=0.3)
#    fill = styles.PatternFill(patternType='solid', fgColor=fill_color)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def do_header(sheet):
    
    sheet.column_dimensions['A'].width = 40
    sheet.column_dimensions['C'].width = 10
    sheet.column_dimensions['D'].width = 20

    # sheet.title = title

    header = [
        # name          width  alignment]
        [ 'Enabled',    8,     'center', ], # 1
        [ 'Disabled',   8,     'center', ],
        [ '',           1,     'center', ],
        [ 'Success',    8,     'center', ],
        [ 'Failure',    8,     'center', ], # 5
        [ 'Unstable',   8,     'center', ],
        [ 'Aborted',    7,     'center', ],
        [ '',           1,     'center', ],
        [ 'SFUA',       None,  'center', ],
        [ 'VIEW',       6,     'center', ], # 10
        [ 'URL',        6,     None      ],
        [ 'TOTAL',      6,     None      ],
    ]

    align = get_aligns()
    font = get_fonts()
    fill = get_fills()

    last_row = 0
    for row in range(1,2):
        last_row = row
        for col in range(1,100):
            cell = sheet.cell(row=row, column=col)
            cell.font = font['yellow']
            cell.fill = fill['purple']

    # c.fill = PatternFill('gray0625')                  # DOTTED
    # c.fill = PatternFill('solid', fgColor = 'F2F2F2') # SEPARATOR
    # ws['E7'].fill = GradientFill('linear', stop = ('85E4F7','4617F1'))
    # https://pythoninoffice.com/python-openpyxl-excel-formatting-cells/
    for idx,rec in enumerate(header, start=1):
        letter = chr(ord('A') + idx - 1)
        if rec[1] is not None:
            sheet.column_dimensions[letter].width = rec[1]

        cell = sheet.cell(row=last_row, column=idx)
        cell.value = rec[0]
        if rec[2] is not None:
            cell.alignment = align[rec[2]]

    return

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def do_formulas(sheet, row):
    """ . """

    # worksheet.get_highest_row()
    # worksheet.get_highest_column()

    center = Alignment(horizontal='center',vertical='center')

    col=4
    states = get_states()
    for idx,state in enumerate(states):
        for row in range(2,4):
            cell = sheet.cell(row=row, column=col+idx)
            cell.alignment = center
            if row == 2:
                cell.value = '= COUNTIFS(I6:I%s, "%s")' % (sheet.max_row, state)
            else:
                continue
                # Ranges supported
                # https://openpyxl.readthedocs.io/en/stable/styles.html
                cell.value = '= COUNTIFS(I6:I%s, "%s")' % (sheet.max_row, state)
                cell.style = percent

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def gen_spreadsheet(data):
    """ . """

    workbook = Workbook()
    # sheet = workbook.active

    

# =COUNTIF(range,value)


    row = 2

    job_data = sorted(data.keys())
    for idx, view in enumerate(job_data):
        view = data[view]
        name = view['name']
        
        ## Cannot use literal view name, 4 tabs fill screen
        ws = workbook.create_sheet(title="V%d" % idx)
        
        do_header(ws)
        # do_body_format(ws)

        AFUS = ['SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED']
        for col,state in enumerate(AFUS, start=64):
            cell = ws.cell(row=row, column=col)
            cell.value = len(view[state])
            
            ws.cell(row=row, column=10).value = name

        row = 5
        for state in AFUS:
                
            # for val in sorted(view[state], reverse=True): struct not list
            for val in view[state]:
                
                col  = 9
                row = row + 1
                
                cell = ws.cell(row=row, column=col)
                cell.value = state
                
                col = col + 1
                cell = ws.cell(row=row, column=col)
                
                # https://programtalk.com/vs4/python/birforce/vnpy_crypto/venv/lib/python3.6/site-packages/openpyxl/writer/worksheet.py/
                
                cell.style = "Hyperlink"

                if True:
                    for key,url in val['urls'].items():
                        cell.value = 'view'
                        cell.hyperlink = url
                else:
                    idx = 0
                    hll = HyperlinkList()
                    for key,val in val['urls'].items():
                        link = Hyperlink(val, display= "V%d" % idx)
                        link.display   = "V%d" % idx
                        # link.hyperlink = val
                        idx = idx + 1
                        hll.append(link)
                        
                        # cell.value = hll
                        cell.hyperlink = str(hll.hyperlink)

        # Add total formuals after grid populated and size is known
        do_formulas(ws, 2)

        # Where is this stray tab coming from ?
        junk = workbook.get_sheet_by_name('Sheet')
        workbook.remove_sheet(junk)

        return workbook

## [SEE ALSO]
## ---------------------------------------------------------------------------
# https://stackoverflow.com/questions/39077661/adding-hyperlinks-in-some-cells-openpyxl    
# https://www.soudegesu.com/en/post/python/sheet-excel-with-openpyxl/

# ws2 = hospital_ranking.create_sheet(title = 'California')
# ws2 = hospital_ranking.get_sheet_by_name('California')
## ---------------------------------------------------------------------------

# https://openpyxl.readthedocs.io/en/stable/_modules/openpyxl/worksheet/hyperlink.html

# EOF
