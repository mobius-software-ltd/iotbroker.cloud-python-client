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
from iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *
from iot.mqttsn.mqttsn_classes.FullTopic import *

class WillTopicUpd(object):
    def __init__(self, retain, topic):
        self.retain = retain
        self.topic = topic

    def getLength(self):
        length = 2
        if self.topic is not None:
            length += self.topic.getLength() + 1
            if self.topic.getLength() > 252:
                length += 2
        return length

    def getType(self):
        return MQTTSN_messageType.SN_WILL_TOPIC_UPD.value[0]

    def isRetain(self):
        return self.retain

    def setRetain(self, retain):
        self.retain = retain

    def getTopic(self):
        return self.topic

    def setTopic(self, topic):
        self.topic = topic