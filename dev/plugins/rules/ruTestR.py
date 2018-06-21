"""
Rule Plugin for Testing
"""
from com.Globals import *

import dev.Rule as Rule
import dev.Variable as Variable

#######
# Globals:

RUPID = 'TestRuleR'
PNAME = 'Test Rule R'
PINFO = 'Lorem ipsum dolor sit amet.'

#######

class PluginRule(Rule.PluginRuleBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'G',
            'ENABLE':True,
            'TIMER':3000,
            'filter':'',
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
        self.timer_period = 2.7
        #self._variable_tick = 0

# -----

    def init(self):
        t = float(self.param['TIMER'])
        if t>0:
            self.timer_period = t
        else:
            self.timer_period = None
        super().init()

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self):
        log(5, 'rugTestR Timer')

# -----

    def variables(self, news:dict):
        log(LOG_INFO, 'Variables in ruTestR: {}', news)

#######
