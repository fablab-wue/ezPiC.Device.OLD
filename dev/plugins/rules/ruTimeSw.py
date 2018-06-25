"""
Rule Plugin for Time Switch
"""
from com.Globals import *

import dev.Rule as Rule
import dev.Variable as Variable
import dev.Timer as Timer

#######
# Globals:

EZPID = 'ruTimeSw'
PTYPE = PT_RULE
PNAME = 'Time Switch'
PINFO = 'Generate (non)retriggerable Pulses triggered by Variable and output to Variable'

#######

class PluginRule(Rule.PluginRuleBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'TimeSwitch',
            'ENABLE':True,
            # instance specific params
            'trigger_key':'Bbbb.Voltage',
            'trigger_val':'',
            'trigger_re':False,
            'out_key':'TimeSwitchOut',
            'out_val_0':'0',
            'out_val_1':'1',
            'out_time':10,
            'if_key':'',
            'if_val':'0',
            'if_com':'=',
            }
        self.timer_period = None
        self.triggered = False

# -----

    def init(self):
        super().init()

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self):
        self.triggered = False
        self.timer_next = None
        Variable.set(self.param['out_key'], self.param['out_val_0'])
        log(LOG_DEBUG, 'TimeSwitch reset')

# -----

    def variables(self, news:dict):

        trigger_key = self.param['trigger_key']
        if not trigger_key: return

        if trigger_key not in news: return

        new_val = news[trigger_key]
        trigger_val = self.param['trigger_val']
        if trigger_val and trigger_val != new_val: return

        #TODO if..

        out_time = int(float(self.param['out_time'])*1000) #TODO
        if self.triggered:
            trigger_re = self.param['trigger_re']
            #TODO retrigger
            self.timer_next = Timer.clock() + out_time

        else:
            self.triggered = True
            self.timer_next = Timer.clock() + out_time

            Variable.set(self.param['out_key'], self.param['out_val_1'])
            log(LOG_DEBUG, 'TimeSwitch for trigger {}', trigger_key)

#######
