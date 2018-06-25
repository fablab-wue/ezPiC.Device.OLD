"""
Gateway Plugin for Testing
"""
from com.Globals import *

import com.Tool as Tool
import dev.Gateway as Gateway
import dev.Variable as Variable

#######
# Globals:

EZPID = 'gwFileLogger'
PTYPE = PT_GATEWAY
PNAME = 'Data Logger to File'
PINFO = 'Log all/filtered Variables to Text File (CSV)'

#######

class PluginGateway(Gateway.PluginGatewayBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'Logger',
            'ENABLE':False,
            'TIMER':0,
            'filter':'',
            # instance specific params
            'file_name':'Logger.log',
            'separator':',',
            }
        self.timer_period = 0
        self._variable_tick = 0
        self._variable_filter = Variable.Filter()

# -----

    def init(self):
        t = float(self.param['TIMER'])
        if t>0:
            self.timer_period = t
        else:
            self.timer_period = None
        super().init()

        self._variable_filter.init(self.param['filter'])

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self):
        log(5, 'gwLogger Timer')

# -----

    def variables(self, news:dict):
        separator = self.param['separator']
        try:
            if Variable.is_new(self._variable_tick):
                self._variable_tick, _news = Variable.get_news_full(self._variable_tick)
                with open(self.param['file_name'], 'a') as f:
                    for key, data in _news.items():
                        if not self._variable_filter.fits(key):
                            continue

                        t = data['time']
                        str_log = time_to_str(t)
                        str_log += separator
                        str_log += key
                        str_log += separator
                        str_log += str(data['value'])
                        log(LOG_DEBUG, 'Logger: {}', str_log)

                        str_log += '\n'
                        b = f.write(str_log)
            pass
        except:
            pass

#######
