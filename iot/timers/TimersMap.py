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
from venv.iot.timers.TimerTask import *
from venv.iot.coap.tlv.CoapMessage import *
from venv.iot.amqp.header.impl.AMQPTransfer import *

class TimersMap():
    def __init__(self, client):
        self.client = client
        self.connectTimer = None
        self.pingTimer = None
        self.timeoutTimer = None
        self.count = 0
        self.timersMap = {}

    def goConnectTimer(self, message):
        if self.connectTimer is not None:
            self.connectTimer.stop()
        self.connectTimer = TimerTask(message, 3, self.client)
        self.connectTimer.start()

    def stopConnectTimer(self):
        if self.connectTimer is not None:
            self.connectTimer.stop()
            self.connectTimer = None

    def goPingTimer(self, message, keepalive):
        if self.pingTimer is not None:
            self.pingTimer.stop()

        self.pingTimer = TimerTask(message, keepalive, self.client)
        self.pingTimer.start()

    def stopPingTimer(self):
        if self.pingTimer is not None:
            self.pingTimer.stop()
            self.pingTimer = None

    def goTimeoutTimer(self):
        if self.timeoutTimer is not None:
            self.timeoutTimer.stop()

        self.timeoutTimer = TimerTask(None, 3, self.client)
        self.timeoutTimer.isTimeoutTask = True
        self.timeoutTimer.start()

    def stopTimeoutTimer(self):
        if self.timeoutTimer is not None:
            self.timeoutTimer.stop()
            self.timeoutTimer = None

    def goMessageTimer(self, message):
        if len(self.timersMap) == 1000:
            raise ValueError('TimersMap : Outgoing identifier overflow')

        if isinstance(message, AMQPTransfer):
            message.setDeliveryId(np.int64(self.getNewPacketID()))
            timer = TimerTask(message, 3, self.client)
            self.timersMap[message.getDeliveryId()] = timer
            timer.start()
            return message.getDeliveryId()
        else:
            if str(type(message).__name__) != 'dict':

                if message.packetID == 0:
                    message.packetID = self.getNewPacketID()
                    if isinstance(message, CoapMessage):
                        message.token = str(message.packetID)

                timer = TimerTask(message, 5, self.client)
                self.timersMap[message.packetID] = timer
                timer.start()
                return message.packetID
            else:
                if message['packetID'] == None:
                    message['packetID'] = self.getNewPacketID()

                timer = TimerTask(message, 3, self.client)
                self.timersMap[message['packetID']] = timer
                timer.start()
                return message['packetID']

    def removeTimer(self, id):
        timer = self.timersMap.get(id)
        if timer is None:
            return None

        message = timer.getMessage()
        timer.stop()
        return message

    def stopTimer(self, id):
        timer = self.timersMap[id]
        if timer is not None:
            message = timer.getMessage()
            timer.stop()
            return message
        return None

    def stopAllTimers(self):
        self.stopConnectTimer()
        self.stopPingTimer()
        self.stopTimeoutTimer()

        for timer in self.timersMap.values():
            if timer is not None:
                timer.stop()

        self.timersMap = {}
        self.count = 0

    def getNewPacketID(self):
        self.count += 1

        if self.count > 65535:
            self.count = 1

        return self.count


