"""
Gateway Plugin for Testing
"""
from com.Globals import *

import dev.Gateway as Gateway
import dev.Variable as Variable

#######
# Globals:

EZPID = 'gwTestGatewayG'
PTYPE = PT_GATEWAY
PNAME = 'Test Gateway G'
PINFO = 'Lorem ipsum dolor sit amet.'

#######

class PluginGateway(Gateway.PluginGatewayBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'G',
            'ENABLE':False,
            'TIMER':3000,
            'FILTER':'',
            # instance specific params
            'name_t':'T',
            'name_h':'H',
            'name_p':'P',
            'abc':123,
            'xyz':456,
            'sel':2,
            'qwe':'Lorem ipsum',
            'asd':[1,2,3,4,5],
            }
        #self._variable_tick = 0

# -----

    def init(self):
        super().init()

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self):
        log(5, 'gwTestG Timer')

# -----

    def variables(self, news:dict):
        log(LOG_INFO, 'Variables in gwTestG: {}', news)

#######
