"""
 # Mobius Software LTD
 # Copyright 2015-2018, Mobius Software LTD
 #
 # This is free software; you can redistribute it and/or modify it
 # under the terms of the GNU Lesser General Public License as
 # published by the Free Software Foundation; either version 2.1 of
 # the License, or (at your option) any later version.
 #
 # This software is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this software; if not, write to the Free
 # Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 # 02110-1301 USA, or see the FSF site: http://www.fsf.org.
"""
from iot.classes.ConnectionState import *
from iot.mqtt.mqtt_messages.MQPublish import *
from iot.mqtt.mqtt_messages.MQPingreq import *
from iot.mqttsn.mqttsn_messages.SNPingreq import *
from iot.amqp.header.impl.AMQPPing import *
from twisted.internet import reactor
from iot.coap.CoapParser import *


class TimerTask():
    def __init__(self, message, period, client, is_connect_timer, is_ping_timer):
        self.message = message
        self.period = period
        self.status = None
        self.isTimeoutTask = False
        self.client = client
        self.active = True
        self.count = 3
        self.is_connect_timer = is_connect_timer
        self.is_ping_timer = is_ping_timer
        if not is_ping_timer and self.message is not None and self.client.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            self.client.send(self.message)

    def handle_function(self):
        if self.active:
            self.onTimedEvent()
            self.client.clientGUI.after(self.period * 1000, self.handle_function)
            self.count -= 1

            if self.is_connect_timer and self.count <= 0:
                self.active = False
                self.client.connectTimeoutMethod()

    def getPeriod(self):
        return self.period

    def getMessage(self):
        return self.message

    def setIsTimeoutTask(self, value):
        self.isTimeoutTask = value

    def start(self):
        if self.active:
            reactor.callFromThread(self.client.clientGUI.after, self.period * 1000, self.handle_function)

    def onTimedEvent(self):

        if self.message is None or not self.active:
            return

        if self.isTimeoutTask:
            self.client.timeoutMethod()

        if self.client.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            if self.status:
                if isinstance(self.message, MQPublish):
                    self.message.dup = True

            self.client.send(self.message)

    def stop(self):
        self.active = False
