"""
Gateway Plugin for Testing
"""
#https://www.home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/


import paho.mqtt.client as mqtt

from com.Globals import *

import com.Tool as Tool
import dev.Gateway as Gateway
import dev.Variable as Variable

#######
# Globals:

EZPID = 'gwMQTT'
PTYPE = PT_GATEWAY
PNAME = 'To MQTT Broker'
PINFO = '???'

#######

class PluginGateway(Gateway.PluginGatewayBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0,
            'filter':'',
            # instance specific params
            'mqtt_broker':'iot.eclipse.org',
            'mqtt_port':1883,
            'mqtt_user':'',
            'mqtt_pw':'',
            'mqtt_qos':0,
            'sub_topic':'/#',
            'sub_var_prefix':'MQTT',
            'pub_topic_prefix':'/',

            'file_name':'Logger.log',
            'separator':',',
            }
        self._variable_tick = 0
        self._variable_filter = Variable.Filter()

        self._client = None

# =====

    # The callback for when the client receives a CONNACK response from the server.
    @staticmethod
    def on_connect(client, self, flags, rc):
        log(LOG_DEBUG, 'MQTT connect: {}', str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        #client.subscribe("$SYS/#")
        client.subscribe("/12345/#")

# -----

    # The callback for when a PUBLISH message is received from the server.
    @staticmethod
    def on_message(client, self, msg):
        topic = msg.topic.replace('/', '.')
        payload = msg.payload.decode()
        print(topic+"     "+payload)
        Variable.set(topic, payload, 'MQTT')

# =====



    def init(self):
        if not self._client:
            self._client = mqtt.Client(client_id='ich2', userdata=self)
            self._client.on_connect = PluginGateway.on_connect
            self._client.on_message = PluginGateway.on_message

        self._client.username_pw_set(username='', password=None)
        self._client.connect_async("iot.eclipse.org", 1883, 60)
        self._client.loop_start()

        super().init()

        self._variable_filter.init(self.param['filter'])

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self):
        #log(5, 'gwLogger Timer')
        pass

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
                        #log(LOG_DEBUG, 'Logger: {}', str_log)

                        #str_log += '\n'
                        #b = f.write(str_log)
            pass
        except:
            pass

#######
