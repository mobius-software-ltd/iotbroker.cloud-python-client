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
from threading import Timer
from venv.iot.classes.ConnectionState import *
from venv.iot.mqtt.mqtt_messages.MQPublish import *

class TimerTask():
    def __init__(self, message, period, client):
        self.message = message
        self.period = period
        self.timer = Timer(self.period, self.handle_function)
        self.status = None
        self.isTimeoutTask = False
        self.client = client
        self.client.send(self.message)

    def handle_function(self):
        self.onTimedEvent()
        self.timer = Timer(self.period, self.handle_function)
        self.timer.start()

    def getPeriod(self):
        return self.period

    def getMessage(self):
        return self.message

    def setIsTimeoutTask(self, value):
        self.isTimeoutTask = value

    def start(self):
        self.timer.start()

    def onTimedEvent(self):
        if self.isTimeoutTask == True:
            self.client.timeoutMethod()

        if self.client.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            if self.status == True:
                if isinstance(self.message, MQPublish):
                    self.message.dup = True

            self.client.send(self.message)
            self.status = True

    def stop(self):
        self.timer.cancel()