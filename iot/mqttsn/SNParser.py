from venv.iot.mqttsn.mqttsn_messages.Advertise import *
from venv.iot.mqttsn.mqttsn_messages.Encapsulated import *
from venv.iot.mqttsn.mqttsn_messages.GWInfo import *
from venv.iot.mqttsn.mqttsn_messages.Regack import *
from venv.iot.mqttsn.mqttsn_messages.Register import *
from venv.iot.mqttsn.mqttsn_messages.SearchGW import *
from venv.iot.mqttsn.mqttsn_messages.SNConnack import *
from venv.iot.mqttsn.mqttsn_messages.SNConnect import *
from venv.iot.mqttsn.mqttsn_messages.SNDisconnect import *
from venv.iot.mqttsn.mqttsn_messages.SNPingreq import *
from venv.iot.mqttsn.mqttsn_messages.SNPingresp import *
from venv.iot.mqttsn.mqttsn_messages.SNPuback import *
from venv.iot.mqttsn.mqttsn_messages.SNPubcomp import *
from venv.iot.mqttsn.mqttsn_messages.SNUnsuback import *
from venv.iot.mqttsn.mqttsn_messages.SNPublish import *
from venv.iot.mqttsn.mqttsn_messages.SNPubrec import *
from venv.iot.mqttsn.mqttsn_messages.SNPubrel import *
from venv.iot.mqttsn.mqttsn_messages.SNSuback import *
from venv.iot.mqttsn.mqttsn_messages.SNSubscribe import *
from venv.iot.mqttsn.mqttsn_messages.SNUnsubscribe import *
from venv.iot.mqttsn.mqttsn_messages.WillMsg import *
from venv.iot.mqttsn.mqttsn_messages.WillMsgReq import *
from venv.iot.mqttsn.mqttsn_messages.WillMsgResp import *
from venv.iot.mqttsn.mqttsn_messages.WillMsgUpd import *
from venv.iot.mqttsn.mqttsn_messages.WillTopic import *
from venv.iot.mqttsn.mqttsn_messages.WillTopicReq import *
from venv.iot.mqttsn.mqttsn_messages.WillTopicResp import *
from venv.iot.mqttsn.mqttsn_messages.WillTopicUpd import *

from venv.iot.mqttsn.mqttsn_classes.Flags import *
from venv.iot.mqttsn.mqttsn_classes.Controls import *
from venv.iot.mqttsn.mqttsn_classes.FullTopic import *
from venv.iot.mqttsn.mqttsn_classes.ShortTopic import *
from venv.iot.mqttsn.mqttsn_classes.IdentifierTopic import *

from venv.iot.mqtt.mqtt_classes.MQTopic import *

import struct

class SNParser(object):
    def __init__(self, message):
        if message is not None:
            self.message = message
        self.index = 0
        self.length = 0

    def setMessage(self, message):
        if message is not None:
            self.message = message

    def encode(self):
        messageType = self.message.getType()
        buffer = encode_messageType_method(self, messageType, self.message)
        return buffer

    def decode(self, data):
        self.buffer = bytearray(data)
        length, index = self.decodeContentLength()
        self.index = index
        self.length = length
        messageType = struct.unpack('B',self.buffer[index:index+1])
        self.index += 1
        messageReturn = decode_messageType_method(self, messageType[0])
        self.index = 0
        return messageReturn

    def decodeContentLength(self):
        length = self.length
        index = self.index
        firstByte = struct.unpack('B', self.buffer[index:index+1])
        if firstByte[0] == 1:
            length = getShort(self.buffer[index+1:index+3])
            index += 3
        else:
            length = firstByte[0]
            index += 1
        return length, index

def ADVERTISE(self, message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, Advertise):
        data = addByte(data, int(message.getType()))
        data = addByte(data, int(message.getgwID()))
        data = addShort(data, int(message.getDuration()))
    else:
        raise ValueError('Encode.advertise malformed message')

    return data

def SEARCHGW(self, message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SearchGW):
        data = addByte(data, int(message.getType()))
        data = addByte(data, int(message.getRadius()))
    else:
        raise ValueError('Encode.searchGW malformed message')
    return data

def GWINFO(self, message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, GWInfo):
        data = addByte(data, int(message.getType()))
        data = addByte(data, message.getgwID())
        if message.getgwAddress() is not None and len(message.getgwAddress())>0:
            data = addString(data, message.getgwAddress())
    else:
        raise ValueError('Encode.gwInfo malformed message')
    return data

def CONNECT(self, message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNConnect):
        data = addByte(data, int(message.getType()))
        flags = Flags(False, None, False, message.getWillPresent(), message.getCleanSession(), None)
        flagsByte = flags.encode()
        data = addByte(data, flagsByte)
        data = addByte(data, message.getProtocolID())
        data = addShort(data, message.getDuration())
        data = addString(data, message.getClientID())
    else:
        raise ValueError('Encode.snConnect malformed message')
    return data

def CONNACK(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNConnack):
        data = addByte(data, int(message.getType()))
        data = addByte(data, message.getCode())
    else:
        raise ValueError('Encode.connack malformed message')
    return data

def WILL_TOPIC_RESP(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, WillTopicResp):
        data = addByte(data, int(message.getType()))
        data = addByte(data, message.getCode())
    else:
        raise ValueError('Encode.willTopicResp malformed message')
    return data

def WILL_MSG_RESP(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, WillMsgResp):
        data = addByte(data, int(message.getType()))
        data = addByte(data, message.getCode())
    else:
        raise ValueError('Encode.willMsgResp malformed message')
    return data

def WILL_TOPIC(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())
    if isinstance(message, WillTopic):
        data = addByte(data, int(message.getType()))
        if message.getTopic() is not None:
            flags = Flags(False, message.getTopic().getQoS(), message.isRetain(), False, False, message.getTopic().getType())
            flagsByte = flags.encode()
            data = addByte(data, flagsByte)
            data = addString(data, message.getTopic().getValue())
            return data
    else:
        raise ValueError('Encode.willTopic malformed message')

def WILL_MSG(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, WillMsg):
        data = addByte(data, int(message.getType()))
        data = addString(data, message.getContent())
    else:
        raise ValueError('Encode.willMsgResp malformed message')
    return data

def REGISTER(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, Register):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getTopicID())
        data = addShort(data, message.getPacketID())
        data = addString(data, message.getTopicName())
    else:
        raise ValueError('Encode.register malformed message')
    return data

def REGACK(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, Regack):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getTopicID())
        data = addShort(data, message.getPacketID())
        data = addByte(data, message.getCode())
    else:
        raise ValueError('Encode.regack malformed message')
    return data

def PUBLISH(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNPublish):
        data = addByte(data, int(message.getType()))
        topic = message.getTopic()
        if topic is not None:
            flags = Flags(message.isDup(), message.getTopic().getQoS(), message.isRetain(), False, False,
                          message.getTopic().getType())
            flagsByte = flags.encode()
            data = addByte(data, flagsByte)

            if isinstance(topic, FullTopic):
                data = addString(data, message.getTopic().getValue())
            else:
                data = addShort(data, message.getTopic().getValue())

            data = addShort(data, message.getPacketID())
            data = addString(data, message.getContent())
            return data
    else:
        raise ValueError('Encode.publish malformed message')

def PUBACK(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNPuback):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getTopicID())
        data = addShort(data, message.getPacketID())
        data = addByte(data, message.getCode())
    else:
        raise ValueError('Encode.puback malformed message')
    return data

def PUBREC(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNPubrec):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getPacketID())
    else:
        raise ValueError('Encode.pubrec malformed message')
    return data

def PUBREL(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNPubrel):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getPacketID())
    else:
        raise ValueError('Encode.pubrel malformed message')
    return data

def PUBCOMP(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNPubcomp):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getPacketID())
    else:
        raise ValueError('Encode.pubcomp malformed message')
    return data

def UNSUBACK(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNUnsuback):
        data = addByte(data, int(message.getType()))
        data = addShort(data, message.getPacketID())
    else:
        raise ValueError('Encode.unsuback malformed message')
    return data

def SUBSCRIBE(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNSubscribe):
        data = addByte(data, message.getType())
        topic = message.getTopic()
        if topic is not None:
            flags = Flags(message.isDup(), message.getTopic().getQoS(), False, False, False,
                          message.getTopic().getType())
            flagsByte = flags.encode()
            data = addByte(data, flagsByte)
            data = addShort(data, message.getPacketID())

            if isinstance(topic, FullTopic):
                data = addString(data, message.getTopic().getValue())
            else:
                data = addShort(data, message.getTopic().getValue())

            return data
    else:
        raise ValueError('Encode.subscribe malformed message')

def SUBACK(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNSuback):
        data = addByte(data, int(message.getType()))
        flags = Flags(False, message.getQoS(), False, False, False, None)
        flagsByte = flags.encode()
        data = addByte(data, flagsByte)
        data = addShort(data, message.getTopicID())
        data = addShort(data, message.getPacketID())
        data = addByte(data, message.getCode())
        return data
    else:
        raise ValueError('Encode.suback malformed message')

def UNSUBSCRIBE(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, SNUnsubscribe):
        data = addByte(data, int(message.getType()))
        if message.getTopic() is not None:
            flags = Flags(False,message.getTopic().getQoS(),False,False,False,message.getTopic().getType())
            flagsByte = flags.encode()
            data = addByte(data, flagsByte)
            data = addShort(data, message.getPacketID())
            data = addString(data, message.getTopic().getValue())
            return data
    else:
        raise ValueError('Encode.unsubscribe malformed message')

def PINGREQ(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if message.getLength() > 2:
        if isinstance(message, SNPingreq):
            data = addByte(data, int(message.getType()))
            data = addString(data, message.getClientID())
            return data
        else:
            raise ValueError('Encode.pingReq malformed message')
    else:
        return data

def DISCONNECT(self,message):
    data = bytearray()
    data = addByte(data, message.getLength())
    if isinstance(message, SNDisonnect):
        data = addByte(data, int(message.getType()))
        if message.getLength() > 2:
            data = addShort(data, message.getDuration())
        return data
    else:
        raise ValueError('Encode.disconnect malformed message')

def WILL_TOPIC_UPD(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, WillTopicUpd):
        data = addByte(data, int(message.getType()))
        if message.getTopic() is not None:
            flags = Flags(False,message.getTopic().getQoS(),message.isRetain(),False,False,None)
            flagsByte = flags.encode()
            data = addByte(data, flagsByte)
            data = addString(data, message.getTopic().getValue())
            return data
    else:
        raise ValueError('Encode.willTopicUpd malformed message')

def WILL_MSG_UPD(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, WillMsgUpd):
        data = addByte(data, int(message.getType()))
        if message.getContent() is not None:
            data = addString(data, message.getContent())
            return data
    else:
        raise ValueError('Encode.willMsgUpd malformed message')

def WILL_TOPIC_REQ(self,message):
    raise ValueError('Encode.willTopicReq not parse message')

def WILL_MSG_REQ(self,message):
    raise ValueError('Encode.willMsgReq not parse message')

def PINGRESP(self,message):
    raise ValueError('Encode.pingResp not parse message')

def ENCAPSULATED(self,message):
    data = bytearray()
    if message.getLength() <= 255:
        data = addByte(data, message.getLength())
    else:
        data = addByte(data, 1)
        data = addShort(data, message.getLength())

    if isinstance(message, Encapsulated):
        data = addByte(data, int(message.getType()))
        data = addByte(data, Controls.encode(message.getRadius()))
        data = addString(data, message.getWirelessNodeID())
        data = addString(data, message.getMessage())
        return data
    else:
        raise ValueError('Encode.willMsgUpd malformed message')

switcherEncode = {
        0: ADVERTISE,
        1: SEARCHGW,
        2: GWINFO,
        4: CONNECT,
        5: CONNACK,
        6: WILL_TOPIC_REQ,
        7: WILL_TOPIC,
        8: WILL_MSG_REQ,
        9: WILL_MSG,
        10: REGISTER,
        11: REGACK,
        12: PUBLISH,
        13: PUBACK,
        14: PUBCOMP,
        15: PUBREC,
        16: PUBREL,
        18: SUBSCRIBE,
        19: SUBACK,
        20: UNSUBSCRIBE,
        21: UNSUBACK,
        22: PINGREQ,
        23: PINGRESP,
        24: DISCONNECT,
        26: WILL_TOPIC_UPD,
        27: WILL_TOPIC_RESP,
        28: WILL_MSG_UPD,
        29: WILL_MSG_RESP,
        254: ENCAPSULATED
    }

def encode_messageType_method(self, argument, message):
    return switcherEncode[argument].__call__(self, message)

def ADVERTISE_DECODE(self):
    data = bytearray(self.buffer)
    gwId = getByte(data,self.index)
    duration = getShort(data[self.index+1:self.index+3])
    message = Advertise(gwId, duration)
    return message

def SEARCHGW_DECODE(self):
    data = bytearray(self.buffer)
    radius = getByte(data,self.index)
    message = SearchGW(radius)
    return message

def GWINFO_DECODE(self):
    data = bytearray(self.buffer)
    infogwId = getByte(data, self.index)
    if self.index+1 < self.length:
        gwInfoAddress = getString(data[self.index+1:len(data)])
        gwInfoAddress = gwInfoAddress.strip()
    message = GWInfo(infogwId, gwInfoAddress)
    return message

def CONNECT_DECODE(self):
    data = bytearray(self.buffer)
    decodeFlags = Flags(False, None, False, False, False, None)
    flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_CONNECT)
    self.index += 1
    protocolID = getByte(data, self.index)
    if protocolID != 1:
        raise ValueError('Invalid protocolID ' + protocolID)
    self.index += 1
    duration = getShort(data[self.index:self.index + 2])
    self.index += 2
    clientID = getString(data[self.index:len(data)])
    clientID = clientID.strip()
    message = SNConnect(flags.isWill(), flags.isClean(), duration, clientID)
    return message

def CONNACK_DECODE(self):
    data = bytearray(self.buffer)
    code = getByte(data, self.index)
    message = SNConnack(code)
    return message

def WILL_TOPIC_REQ_DECODE(self):
    data = bytearray(self.buffer)
    message = WillTopicReq()
    return message

def WILL_TOPIC_DECODE(self):
    data = bytearray(self.buffer)
    retain = False
    willTopic = None
    if self.index < len(data):
        decodeFlags = Flags(False, None, False, False, False, None)
        flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_WILL_TOPIC)
        self.index += 1
        retain = flags.isRetain()
        value = getString(data[self.index:len(data)])
        value = value.strip()
        willTopic = FullTopic(value, flags.getQoS())
    message = WillTopic(retain, willTopic)
    return message

def WILL_MSG_REQ_DECODE(self):
    data = bytearray(self.buffer)
    message = WillMsgReq()
    return message

def WILL_MSG_DECODE(self):
    data = bytearray(self.buffer)
    if self.index < len(data):
        content = getString(data[self.index:len(data)])
    message = WillMsg(content)
    return message

def REGISTER_DECODE(self):
    data = bytearray(self.buffer)
    topicID = getShort(data[self.index:self.index + 2])
    self.index += 2
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    if self.index < self.length:
        topicName = getString(data[self.index:len(data)])
    message = Register(topicID, messageID, topicName)
    return message

def REGACK_DECODE(self):
    data = bytearray(self.buffer)
    topicID = getShort(data[self.index:self.index + 2])
    self.index += 2
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    code = getByte(data,self.index)
    message = Regack(topicID, messageID, code)
    return message

def PUBLISH_DECODE(self):
    data = bytearray(self.buffer)
    decodeFlags = Flags(False, None, False, False, False, None)
    flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_PUBLISH)
    self.index += 1
    topicID = getShort(data[self.index:self.index + 2])
    self.index += 2
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    if flags.getQoS() != 0 and messageID == 0:
        raise ValueError('invalid PUBLISH QoS-0 messageID: ' + messageID)
    topic = None
    if flags.getTopicType() == TopicType.SHORT: #SHORT
        topic = ShortTopic(topicID, flags.getQoS())
    else:
        topic = IdentifierTopic(topicID, flags.getQoS())
    content = ''
    if self.index < self.length:
        content = getString(data[self.index:len(data)])
        content.strip()
    message = SNPublish(messageID,topic,content,flags.isDup(),flags.isRetain())
    return message

def PUBACK_DECODE(self):
    data = bytearray(self.buffer)
    topicID = getShort(data[self.index:self.index + 2])
    self.index += 2
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    code = getByte(data, self.index)
    message = SNPuback(topicID, messageID, code)
    return message

def PUBREC_DECODE(self):
    data = bytearray(self.buffer)
    messageID = getShort(data[self.index:self.index + 2])
    message = SNPubrec(messageID)
    return message

def PUBREL_DECODE(self):
    data = bytearray(self.buffer)
    messageID = getShort(data[self.index:self.index + 2])
    message = SNPubrel(messageID)
    return message

def PUBCOMP_DECODE(self):
    data = bytearray(self.buffer)
    messageID = getShort(data[self.index:self.index + 2])
    message = SNPubcomp(messageID)
    return message

def SUBSCRIBE_DECODE(self):
    data = bytearray(self.buffer)
    decodeFlags = Flags(False, None, False, False, False, None)
    flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_WILL_TOPIC)
    self.index += 1
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    topic = None
    if self.index < self.length:
        if flags.getTopicType() == TopicType.NAMED:
            topicName = getString(data[self.index:len(data)])
            topic = FullTopic(topicName, flags.getQoS())
        if flags.getTopicType() == TopicType.ID:
            topicID = getShort(data[self.index:self.index + 2])
            topic = IdentifierTopic(topicName, flags.getQoS())
        if flags.getTopicType() == TopicType.SHORT:
            topicID = getShort(data[self.index:self.index + 2])
            topic = ShortTopic(topicID, flags.getQoS())
    message = SNSubscribe(messageID, topic, flags.isDup())
    return message

def SUBACK_DECODE(self):
    data = bytearray(self.buffer)
    decodeFlags = Flags(False, None, False, False, False, None)
    flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_SUBACK)
    self.index += 1
    topicID = getShort(data[self.index:self.index + 2])
    self.index += 2
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    code = getByte(data, self.index)
    message = SNSuback(topicID, code, flags.getQoS(), messageID)
    return message

def UNSUBSCRIBE_DECODE(self):
    data = bytearray(self.buffer)
    decodeFlags = Flags(False, None, False, False, False, None)
    flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_UNSUBSCRIBE)
    self.index += 1
    messageID = getShort(data[self.index:self.index + 2])
    self.index += 2
    topic = None
    if self.index < self.length:
        if flags.getTopicType() == TopicType.NAMED:
            topicName = getString(data[self.index:len(data)])
            topic = FullTopic(topicName, flags.getQoS())
        if flags.getTopicType() == TopicType.ID: #ID
            topicID = getShort(data[self.index:self.index + 2])
            topic = IdentifierTopic(topicName, flags.getQoS())
        if flags.getTopicType() == TopicType.SHORT: #SHORT
            topicName = getString(data[self.index:len(data)])
            topic = ShortTopic(topicName, flags.getQoS())
    message = SNUnsubscribe(messageID, topic)
    return message

def UNSUBACK_DECODE(self):
    data = bytearray(self.buffer)
    messageID = getShort(data[self.index:self.index + 2])
    message = SNUnsuback(messageID)
    return message

def PINGREQ_DECODE(self):
    data = bytearray(self.buffer)
    clientID = None
    if self.index < self.length:
        clientID = getString(data[self.index:len(data)])
    message = SNPingreq(clientID.strip())
    return message

def PINGRESP_DECODE(self):
    data = bytearray(self.buffer)
    message = SNPingresp()
    return message

def DISCONNECT_DECODE(self):
    data = bytearray(self.buffer)
    duration = 0
    if self.index < self.length:
        duration = getShort(data[self.index:self.index + 2])
    message = SNDisonnect(duration)
    return message

def WILL_TOPIC_UPD_DECODE(self):
    data = bytearray(self.buffer)
    topic = None
    retain = False
    if self.index < self.length:
        decodeFlags = Flags(False, None, False, False, False, None)
        flags = decodeFlags.decode(getByte(data, self.index), MQTTSN_messageType.SN_WILL_TOPIC_UPD)
        self.index += 1
        retain = flags.isRetain()
        value = getString(data[self.index:len(data)])
        topic = FullTopic(value, flags.getQoS())
    message = WillTopicUpd(retain, topic)
    return message

def WILL_MSG_UPD_DECODE(self):
    data = bytearray(self.buffer)
    content = ''
    if self.index < self.length:
        content = getString(data[self.index:len(data)])
    message = WillMsgUpd(content)
    return message

def WILL_TOPIC_RESP_DECODE(self):
    print('HERE')
    data = bytearray(self.buffer)
    code = getByte(data, self.index)
    message = WillTopicResp(code)
    return message

def WILL_MSG_RESP_DECODE(self):
    data = bytearray(self.buffer)
    code = getByte(data, self.index)
    message = WillMsgResp(code)
    return message

def ENCAPSULATED_DECODE(self):
    raise ValueError('Encapsulated.decode ')

switcherDecode = {
        0: ADVERTISE_DECODE,
        1: SEARCHGW_DECODE,
        2: GWINFO_DECODE,
        4: CONNECT_DECODE,
        5: CONNACK_DECODE,
        6: WILL_TOPIC_REQ_DECODE,
        7: WILL_TOPIC_DECODE,
        8: WILL_MSG_REQ_DECODE,
        9: WILL_MSG_DECODE,
        10: REGISTER_DECODE,
        11: REGACK_DECODE,
        12: PUBLISH_DECODE,
        13: PUBACK_DECODE,
        14: PUBCOMP_DECODE,
        15: PUBREC_DECODE,
        16: PUBREL_DECODE,
        18: SUBSCRIBE_DECODE,
        19: SUBACK_DECODE,
        20: UNSUBSCRIBE_DECODE,
        21: UNSUBACK_DECODE,
        22: PINGREQ_DECODE,
        23: PINGRESP_DECODE,
        24: DISCONNECT_DECODE,
        26: WILL_TOPIC_UPD_DECODE,
        27: WILL_TOPIC_RESP_DECODE,
        28: WILL_MSG_UPD_DECODE,
        29: WILL_MSG_RESP_DECODE,
        254: ENCAPSULATED_DECODE
    }

def decode_messageType_method(self, argument):
    return switcherDecode[argument].__call__(self)

def addByte(data, byte):
    data.append(byte)
    return data

def getByte(data, index):
    tuple = struct.unpack('B', data[index: index+1])
    return tuple[0]

def addShort(data, short):
    dataStruct  = struct.pack('h', short)
    data += dataStruct[::-1]
    return data

def getShort(data):
    tuple = struct.unpack('h', data[::-1])
    return tuple[0]

def addString(dataIn, text):
    #data = addShort(dataIn, len(text))
    data = dataIn
    for ch in text:
        ch = bytes(ch, encoding='utf_8')
        data += struct.pack('c', ch)
    return data

def getString(data):
    return data.decode('utf_8')