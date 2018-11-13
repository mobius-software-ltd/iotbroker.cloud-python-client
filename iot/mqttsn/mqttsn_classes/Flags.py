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
from venv.iot.classes.QoSType import *
from venv.iot.mqttsn.mqttsn_classes.Flag import *
from venv.iot.mqttsn.mqttsn_classes.Flags import *
from venv.iot.mqttsn.mqttsn_classes.TopicType import *
from venv.iot.mqttsn.mqttsn_classes.MQTTSN_messageType import *

class Flags():
    def __init__(self, dup, qos, retain, will, cleanSession, topicType):

        self.dup = dup
        if qos is not None:
            self.qos = qos
        else:
            self.qos = None
        self.retain = retain
        self.will = will
        self.cleanSession = cleanSession
        self.topicType = topicType

    def isDup(self):
        return self.dup

    def setDup(self, dup):
        self.dup = dup

    def getQoS(self):
        return self.qos

    def setQoS(self, qos):
        self.qos = qos

    def isRetain(self):
        return self.retain

    def setRetain(self, retain):
        self.retain = retain

    def isWill(self):
        return self.will

    def setWill(self, will):
        self.will = will

    def isClean(self):
        return self.cleanSession

    def setClean(self, clean):
        self.cleanSession = clean

    def getTopicType(self):
        return self.topicType

    def setTopicType(self, topicType):
        self.topicType = topicType

    def encode(self):
        flagsByte = 0
        if self.dup:
            flagsByte += 128 #Flag.DUPLICATE
        if self.qos is not None:
            flagsByte += self.qos.getValue() << 5
        if self.retain:
            flagsByte += 16 #Flag.RETAIN
        if self.isWill():
            flagsByte += 8 #Flag.WILL
        if self.isClean():
            flagsByte += 4 #Flag.CLEAN_SESSION
        if self.topicType is not None:
            flagsByte += self.topicType.value[0]
        return flagsByte

    def decode(self,flagsByte, type):
        flags = []
        bitmask = []
        flags.append(128) #Flag.DUPLICATE
        flags.append(96) #Flag.QOS_LEVEL_ONE
        flags.append(64) #Flag.QOS_2
        flags.append(32) #Flag.QOS_1
        flags.append(16) #Flag.RETAIN
        flags.append(8) #Flag.WILL
        flags.append(4) #Flag.CLEAN_SESSION
        flags.append(3) #Flag.RESERVED_TOPIC
        flags.append(2) #Flag.SHORT_TOPIC
        flags.append(1) #Flag.ID_TOPIC

        for flag in flags:
            if ((flagsByte & flag) == flag):
                bitmask.append(flag)
        return self.validateAndCreate(bitmask,type)

    def validateAndCreate(self, bitmask, type):
        dup = False
        retain = False
        will = False
        clean = False
        if 3 in bitmask: #RESERVED_TOPIC
            raise ValueError('Error. Reserved flag set to true in SNFlags')
        if 128 in bitmask: #DUPLICATE
            dup = True
        if 16 in bitmask: #RETAIN
            retain = True
        if 8 in bitmask: #WILL
            will = True
        if 4 in bitmask: #CLEAN_SESSION
            clean = True

        qos = QoSType.AT_MOST_ONCE.value[0]
        if Flag.QOS_LEVEL_ONE.value[0] in bitmask:
            qos = QoSType.LEVEL_ONE.value[0]
        if Flag.QOS_2.value[0] in bitmask:
            qos = QoSType.EXACTLY_ONCE.value[0]
        if Flag.QOS_1.value[0] in bitmask:
            qos = QoSType.AT_LEAST_ONCE.value[0]

        topicType = TopicType.NAMED
        if Flag.SHORT_TOPIC.value[0] in bitmask:
            topicType = TopicType.SHORT
        if Flag.ID_TOPIC.value[0] in bitmask:
            topicType = TopicType.ID

        if isinstance(type, MQTTSN_messageType):
            if type == MQTTSN_messageType.SN_CONNECT:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + str(type))
                if qos != QoSType.AT_MOST_ONCE.value[0]:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + str(type))
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            if type == MQTTSN_messageType.SN_WILL_TOPIC:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + str(type))
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + str(type))
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + str(type))
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            if type == MQTTSN_messageType.SN_PUBLISH:
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if dup & (qos == QoSType.AT_MOST_ONCE.value[0] or qos == QoSType.LEVEL_ONE.value[0]):
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + str(type))
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + str(type))
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + str(type))
                if topicType != TopicType.NAMED and topicType != TopicType.SHORT and topicType != TopicType.ID:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            if type == MQTTSN_messageType.SN_SUBSCRIBE:
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if qos == QoSType.LEVEL_ONE.value[0]:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + str(type))
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + str(type))
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + str(type))
                if topicType != TopicType.NAMED and topicType != TopicType.SHORT and topicType != TopicType.ID:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            if type == MQTTSN_messageType.SN_SUBACK:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + str(type))
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + str(type))
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + str(type))
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + str(type))
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            if type == MQTTSN_messageType.SN_UNSUBSCRIBE:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + str(type))
                if qos != QoSType.AT_MOST_ONCE.value[0]:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + str(type))
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + str(type))
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + str(type))
                if topicType != TopicType.NAMED and topicType != TopicType.SHORT and topicType != TopicType.ID:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            if type == MQTTSN_messageType.SN_WILL_TOPIC_UPD:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + str(type))
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + str(type))
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + str(type))
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + str(type))
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + str(type))

            self.dup = dup
            self.retain = retain
            self.qos = qos
            self.will = will
            self.clean = clean
            self.topicType = topicType
            return self