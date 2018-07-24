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
PNAME = 'MQTT - MQTT Client'

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
            'FILTER':'',
            # instance specific params
            'BrokerAddr':'iot.eclipse.org',
            'BrokerPort':1883,
            'BrokerUser':'',
            'BrokerPW':'',
            'SubTopic':'/12345/#',
            'SubVarPrefix':'MQTT.',
            'SubQOS':0,
            'PubTopicPrefix':'/',
            'PubQOS':0,
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
        if self.param['SubTopic']:
            client.subscribe(self.param['SubTopic'], self.param['SubQOS'])

# -----

    # The callback for when a PUBLISH message is received from the server.
    @staticmethod
    def on_message(client, self, msg):
        topic = self.param['SubVarPrefix'] + msg.topic.replace('/', '.')
        payload = msg.payload.decode()
        print(topic+"     "+payload)
        Variable.set(topic, payload, 'MQTT')

# =====

    def init(self):
        if not self._client:
            self._client = mqtt.Client(client_id='ich2', userdata=self)
            self._client.on_connect = PluginGateway.on_connect
            self._client.on_message = PluginGateway.on_message

        self._client.username_pw_set(username=self.param['BrokerUser'], password=self.param['BrokerPW'])
        self._client.connect_async(self.param['BrokerAddr'], self.param['BrokerPort'], 60)
        self._client.loop_start()

        super().init()

        self._variable_filter.init(self.param['FILTER'])

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self):
        #log(5, 'gwLogger Timer')
        pass

# -----

    def variables(self, news:dict):
        if not self._client:
            return
        try:
            #if Variable.is_new(self._variable_tick):
            #self._variable_tick, _news = Variable.get_news(self._variable_tick)
            #for key, data in _news.items():
            for key, data in news.items():
                if not self._variable_filter.fits(key):
                    continue
                if self.param['SubVarPrefix'] and key.startswith(self.param['SubVarPrefix']):
                    continue

                topic = self.param['PubTopicPrefix'] + key.replace('.', '/')
                #data_str = str(data)
                self._client.publish(topic, data, self.param['PubQOS'])
                #log(LOG_DEBUG, 'Logger: {}', str_log)
        except:
            pass

#######
