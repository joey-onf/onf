# -*- python -*-
'''.'''

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
from openpyxl.styles    import Color, PatternFill, Font, Border
from openpyxl.styles    import colors

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##

class Hue:
    '''.'''
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_gradient(self):

        # gradient = PatternFill(fill_type=None,
        # start_color='FFFFFFFF',
        # end_color='FF000000')
        ans = {}
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_color_map(self):

        colors=\
            {  
                # -----------------------------------------
                # https://hexcolorcodes.org/hex-code/9664c8    
                # -----------------------------------------
                'atomic_vomit' : 'D4D977',
                #
                # https://hexcolorcodes.org/hex-code/9664c8    
                'dark_orchid' : '9932CC',
                'medium_orchid' : 'BA55D3',
                'orchidB5'  : 'B570EE',
                #
                'maroon'  : '7C3A5B',
                #
                'orchid_dark'   : '9932CC',
                'orchid_medium' : 'BA55D3',
                'orchid_Br'     : 'B570EE',
                #
                'purple'       : '5F2D91',
                'purple1'      : 'AD2089',
                'purple_C6'    : 'C694F8',
                'purple_AE'    : 'AE7CC0',
                'purple_light' : 'AE7CE0',
                'purple_96'    : '9664C8',
                #
                'red'     : '00FF0000',
                'orange'  : '00FF9000',
                # 'orange'  : 'FFBB00',
                # 'orange' : '00FFBF00',
                # 'dark-orange' : '00D56F00',
                # 'pink'   : '00FFB9C3',
                'pink'   : '00ffe9ec',
                # 'pink'   : '00ff7386',
                'grey'   : 'ecececec',
                # 
                'yellow'  : 'FAFA00',
                'yellow1' : 'FAFA00',
                'yellow2' : 'FFFF48',
            }

        return colors

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_color_hex(self, color:str=None):

        if color is None:
            color = 'atomic_vomit'

        colors = self.get_color_map()
        if color not in colors:
            color = 'atomic_vomit'

        return colors[color]
# [EOF]
