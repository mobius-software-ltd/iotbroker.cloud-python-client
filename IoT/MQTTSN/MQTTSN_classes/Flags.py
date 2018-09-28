from venv.IoT.Classes.QoS import *
from venv.IoT.Classes.QoSType import *
from venv.IoT.MQTTSN.MQTTSN_classes.Flag import *
from venv.IoT.MQTTSN.MQTTSN_classes.Flags import *
from venv.IoT.MQTTSN.MQTTSN_classes.TopicType import *
from venv.IoT.MQTTSN.MQTTSN_classes.MQTTSN_messageType import *

class Flags():
    def __init__(self, dup, qos, retain, will, cleanSession, topicType):
        self.dup = dup
        self.qos = QoS(qos)
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
        self.qos = QoS(qos)

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
            flagsByte += Flag.DUPLICATE
        if self.qos is not None:
            flagsByte += self.qos.getValue() << 5
        if self.retain:
            flagsByte += Flag.RETAIN
        if self.will:
            flagsByte += Flag.WILL
        if self.cleanSession:
            flagsByte += Flag.CLEAN_SESSION
        if self.topicType is not None:
            flagsByte += self.topicType
        return flagsByte

    def decode(self, flagsByte, type):
        flags = []
        bitmask = []
        flags.append(Flag.DUPLICATE)
        flags.append(Flag.QOS_LEVEL_ONE)
        flags.append(Flag.QOS_2)
        flags.append(Flag.QOS_1)
        flags.append(Flag.RETAIN)
        flags.append(Flag.WILL)
        flags.append(Flag.CLEAN_SESSION)
        flags.append(Flag.RESERVED_TOPIC)
        flags.append(Flag.SHORT_TOPIC)
        flags.append(Flag.ID_TOPIC)

        for flag in flags:
            if (flagsByte & flag) == flag:
                bitmask.append(flag)

        return self.validateAndCreate(bitmask,type)

    def validateAndCreate(self, bitmask, type):
        if Flag.RESERVED_TOPIC in bitmask:
            raise ValueError('Error. Reserved flag set to true in SNFlags')
        if Flag.DUPLICATE in bitmask:
            dup = True
        if Flag.RETAIN in bitmask:
            retain = True
        if Flag.WILL in bitmask:
            will = True
        if Flag.CLEAN_SESSION in bitmask:
            clean = True

        qos = QoS(QoSType.AT_MOST_ONCE)
        if Flag.QOS_LEVEL_ONE in bitmask:
            qos = QoS(QoSType.LEVEL_ONE)
        if Flag.QOS_2 in bitmask:
            qos = QoS(QoSType.EXACTLY_ONCE)
        if Flag.QOS_1 in bitmask:
            qos = QoS(QoSType.AT_LEAST_ONCE)

        topicType = TopicType.NAMED
        if Flag.SHORT_TOPIC in bitmask:
            topicType = TopicType.SHORT
        if Flag.ID_TOPIC in bitmask:
            topicType = TopicType.ID

        if isinstance(type, MQTTSN_messageType):
            if type.SN_CONNECT:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + type)
                if qos.getValue() != 0: #AT_MOST_ONCE
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + type)
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            if type.SN_WILL_TOPIC:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + type)
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + type)
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + type)
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            if type.SN_PUBLISH:
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if dup & (qos.getValue() == 0 or qos.getValue() == 3): #AT_MOST_ONCE or LEVEL_ONE
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + type)
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + type)
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + type)
                if topicType != TopicType.NAMED & topicType != TopicType.SHORT & topicType != TopicType.ID:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            if type.SN_SUBSCRIBE:
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if qos.getValue() == 3: #LEVEL_ONE
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + type)
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + type)
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + type)
                if topicType != TopicType.NAMED & topicType != TopicType.SHORT & topicType != TopicType.ID:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            if type.SN_SUBACK:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + type)
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + type)
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + type)
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + type)
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            if type.SN_UNSUBSCRIBE:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + type)
                if qos.getValue() != 0:  #AT_MOST_ONCE
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if retain:
                    raise ValueError('Error. SNFlags. Invalid encoding: retain flag = ' + type)
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + type)
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + type)
                if topicType != TopicType.NAMED & topicType != TopicType.SHORT & topicType != TopicType.ID:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            if type.SN_WILL_TOPIC_UPD:
                if dup:
                    raise ValueError('Error. SNFlags. Invalid encoding: dup flag = ' + type)
                if qos is None:
                    raise ValueError('Error. SNFlags. Invalid encoding: qos flag = ' + type)
                if will:
                    raise ValueError('Error. SNFlags. Invalid encoding: will flag = ' + type)
                if clean:
                    raise ValueError('Error. SNFlags. Invalid encoding: clean flag = ' + type)
                if topicType != TopicType.NAMED:
                    raise ValueError('Error. SNFlags. Invalid encoding: topicType flag = ' + type)

            self.dup = dup
            self.retain = retain
            self.qos = qos
            self.will = will
            self.clean = clean
            self.topicType = topicType
            return self