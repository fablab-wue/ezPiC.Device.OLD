"""
Rule Plugin for Testing
"""
from com.Globals import *

import dev.Rule as Rule
import dev.Variable as Variable

#######
# Globals:

EZPID = 'ruTestRuleR'
PTYPE = PT_RULE
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

# -----

    def init(self):
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
