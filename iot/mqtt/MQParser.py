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
from iot.mqtt.mqtt_messages.MQConnect import *
from iot.mqtt.mqtt_messages.MQConnack import *
from iot.mqtt.mqtt_messages.MQDisconnect import *
from iot.mqtt.mqtt_messages.MQPingreq import *
from iot.mqtt.mqtt_messages.MQPingresp import *
from iot.mqtt.mqtt_messages.MQPuback import *
from iot.mqtt.mqtt_messages.MQPubcomp import *
from iot.mqtt.mqtt_messages.MQPublish import *
from iot.mqtt.mqtt_messages.MQPubrec import *
from iot.mqtt.mqtt_messages.MQPubrel import *
from iot.mqtt.mqtt_messages.MQSuback import *
from iot.mqtt.mqtt_messages.MQSubscribe import *
from iot.mqtt.mqtt_messages.MQUnsuback import *
from iot.mqtt.mqtt_messages.MQUnsubscribe import *

from iot.mqtt.mqtt_classes.MQTopic import *
from iot.mqtt.mqtt_classes.Will import *

import struct
import binascii

class MQParser(object):
    def __init__(self, message):
        if message is not None:
            self.message = message

    def setMessage(self, message):
        if message is not None:
            self.message = message

    def next(self, data, index):

        length = 0
        multiplier = 1
        bytes_used = 0
        while(True):

            if multiplier > 128 * 128 * 128:
                return -1

            if len(data) < index + 1:
                return -1

            enc = data[index]
            index += 1
            length += (enc & 0x7f) * multiplier
            multiplier *= 128
            bytes_used += 1

            if (enc & 0x80) == 0:
                break

        return length + bytes_used + 1

    def encode(self):
        messageType = self.message.getType()
        buffer = encode_messageType_method(self, messageType, self.message)
        return buffer

    def decode(self, data):
        self.buffer = bytearray(data)
        firtsByte = struct.unpack('B', self.buffer[0:1])
        messageType = (firtsByte[0] >> 4) & 0xf
        messageReturn = decode_messageType_method(self, messageType)
        return messageReturn

    def getBufferByLength(self):
        data = bytearray()
        ln = int(self.message.getLength())
        while True:
            byteE = int(ln % 128)
            ln = int(ln / 128)
            if ln > 0:
                data.append(byteE | 128)
            else:
                data.append(byteE)
            if ln <= 0:
                break
        return data


def MQ_CONNECT(self, message):
    data = bytearray()

    data.append(message.getType() << 4)
    data += self.getBufferByLength()

    protocolName = 'MQTT'
    nameData = struct.pack('h', len(protocolName))
    data += nameData[::-1]

    for ch in protocolName:
        ch = bytes(ch, encoding='utf_8')
        data += struct.pack('c', ch)

    data.append(message.protocolLevel)

    contentFlags = 0

    if message.cleanSession == True:
        contentFlags += 2

    if message.willValid() == True:
        contentFlags += 0x04
        qos = message.will.getTopic().getQoS()
        contentFlags += qos.getValue() << 3
        if message.will.getRetain():
            contentFlags += 0x20

    if message.password is not None:
        contentFlags += 0x40

    if message.username is not None:
        contentFlags += 0x80

    data.append(contentFlags)

    keepData = struct.pack('h', int(message.keepAlive))
    data += keepData[::-1]

    clientData = struct.pack('h', len(message.clientID))
    data += clientData[::-1]
    for ch in message.clientID:
        ch = bytes(ch, encoding='utf_8')
        data += struct.pack('c', ch)
    if message.willValid() == True:
        topic = message.will.getTopic()
        if isinstance(topic, MQTopic):
            if topic.getName():
                topicName = topic.getName()
                nameData = struct.pack('h', len(topicName))
                data += nameData[::-1]
                for ch in topicName:
                    ch = bytes(ch, encoding='utf_8')
                    data += struct.pack('c', ch)
            if message.will.content is not None:
                contentTopic = message.will.content
                contentData = struct.pack('h', len(contentTopic))
                data += contentData[::-1]
                for ch in contentTopic:
                    ch = bytes(ch, encoding='utf_8')
                    data += struct.pack('c', ch)

    if message.username is not None:
        userData = struct.pack('h', len(message.username))
        data += userData[::-1]
        for ch in message.username:
            ch = bytes(ch, encoding='utf_8')
            data += struct.pack('c', ch)

    if message.password is not None:
        paswData = struct.pack('h', len(message.password))
        data += paswData[::-1]
        for ch in message.password:
            ch = bytes(ch, encoding='utf_8')
            data += struct.pack('c', ch)

    return data


def MQ_CONNACK(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()
    data.append(message.sessionPresent)
    data.append(message.returnCode)

    return data


def MQ_PUBLISH(self, message):
    data = bytearray()
    firstByte = message.getType() << 4
    if message.dup:
        firstByte |= 8
    else:
        firstByte |= 0
    firstByte |= (message.topic.getQoS().getValue() << 1)
    if message.retain:
        firstByte |= 1
    else:
        firstByte |= 0
    data.append(firstByte)

    data += self.getBufferByLength()
    name = message.topic.name
    nameData = struct.pack('h', len(name))
    data += nameData[::-1]

    for ch in name:
        ch = bytes(ch, encoding='utf-8')
        data += struct.pack('c', ch)

    qos = int(message.topic.getQoS().getValue())
    if qos == 0:  # AT_MOST_ONCE
        if message.packetID != 0:
            raise ValueError('Encode. Publish. Publish qos-0 must not contain packetID')
    if qos in [1, 2]:  # AT_LEAST_ONCE, EXACTLY_ONCE
        packetIDdata = struct.pack('h', message.packetID)
        data += packetIDdata[::-1]

    content = message.content
    for ch in content:
        ch = bytes(ch, encoding='utf-8')
        data += struct.pack('c', ch)
    return data


def MQ_PUBACK(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()
    if message.packetID == 0:
        raise ValueError('Encode. Puback. Puback must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]
    return data


def MQ_PUBREC(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()
    if message.packetID == 0:
        raise ValueError('Encode. Pubrec. Pubrec must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]
    return data


def MQ_PUBREL(self, message):
    data = bytearray()
    data.append(message.getType() << 4 | 0x2)
    data += self.getBufferByLength()
    if message.packetID == 0:
        raise ValueError('Encode. Pubrel. Pubrel must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]
    return data


def MQ_PUBCOMP(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()
    if message.packetID == 0:
        raise ValueError('Encode. Pubcomp. Pubcomp must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]
    return data


def MQ_SUBSCRIBE(self, message):
    data = bytearray()
    data.append(message.getType() << 4 | 0x2)
    data += self.getBufferByLength()

    if message.packetID == 0:
        raise ValueError('Encode. Subscribe. Subscribe must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]

    for topic in message.listMQTopics:
        if isinstance(topic, MQTopic):
            topicData = struct.pack('h', len(topic.name))
            data += topicData[::-1]
            for ch in topic.name:
                ch = bytes(ch, encoding='utf_8')
                data += struct.pack('c', ch)
            data.append(topic.qos.getValue())
    return data


def MQ_SUBACK(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()

    if message.packetID == 0:
        raise ValueError('Encode. Suback. Suback must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]

    for code in message.listCodes:  # list ReturnCodes, SubackCodes
        item = int(code)
        data.append(item)
    return data


def MQ_UNSUBSCRIBE(self, message):
    data = bytearray()
    data.append(message.getType() << 4 | 0x2)
    data += self.getBufferByLength()

    if message.packetID == 0:
        raise ValueError('Encode. Unsubscribe. Unsubscribe must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]

    for name in message.listTopics:
        nameData = struct.pack('h', len(name))
        data += nameData[::-1]
        for ch in name:
            ch = bytes(ch, encoding='utf_8')
            data += struct.pack('c', ch)
    return data


def MQ_UNSUBACK(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()

    if message.packetID == 0:
        raise ValueError('Encode. Unsuback. Unsuback must contain packetID')

    packetIDdata = struct.pack('h', message.packetID)
    data += packetIDdata[::-1]
    return data


def MQ_PINGREQ(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()
    return data


def MQ_PINGRESP(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()

    return data


def MQ_DISCONNECT(self, message):
    data = bytearray()
    data.append(message.getType() << 4)
    data += self.getBufferByLength()
    return data


switcherEncode = {
    1: MQ_CONNECT,
    2: MQ_CONNACK,
    3: MQ_PUBLISH,
    4: MQ_PUBACK,
    5: MQ_PUBREC,
    6: MQ_PUBREL,
    7: MQ_PUBCOMP,
    8: MQ_SUBSCRIBE,
    9: MQ_SUBACK,
    10: MQ_UNSUBSCRIBE,
    11: MQ_UNSUBACK,
    12: MQ_PINGREQ,
    13: MQ_PINGRESP,
    14: MQ_DISCONNECT
}


def encode_messageType_method(self, argument, message):
    return switcherEncode[argument].__call__(self, message)


def MQ_CONNECT_DECODE(self):
    data = bytearray(self.buffer)

    protocolName = data[4:8].decode('utf8')
    if protocolName != 'mqtt':
        raise ValueError('Decode. Connect. Protocol name is wrong')

    protocolLevelTuple = struct.unpack('B', data[8:9])
    protocolLevel = protocolLevelTuple[0]

    contentFlagsTuple = struct.unpack('B', data[9:10])
    contentFlags = contentFlagsTuple[0]

    userNameFlag = (((contentFlags >> 7) & 1)) == 1
    passwordFlag = (((contentFlags >> 6) & 1)) == 1
    willRetainFlag = (((contentFlags >> 5) & 1)) == 1
    willQosFlag = (((contentFlags & 0x1f) >> 3) & 3)
    qos = QoS(willQosFlag)

    if (qos.getValue() < 0) | (qos.getValue() > 2):
        raise ValueError('Decode. Connect. Will QoS set to' + str(qos.getValue()))

    willFlag = (((contentFlags >> 2) & 1)) == 1
    if qos.getValue() > 0 & willFlag != True:
        raise ValueError('Decode. Connect. Will retain set, willFlag not set')

    cleanSessionFlag = (((contentFlags >> 1) & 1)) == 1
    reservedFlag = (contentFlags & 1) == 1

    if reservedFlag == True:
        raise ValueError('Decode. Connect. Reserved flag set to true')

    keepaliveData = data[10:12]
    keepAliveTuple = struct.unpack('h', keepaliveData[::-1])
    keepAlive = keepAliveTuple[0]

    clientIDlenData = data[12:14]
    clientIDlenTuple = struct.unpack('h', clientIDlenData[::-1])
    clientIDlen = clientIDlenTuple[0]
    clientID = data[14:14 + clientIDlen].decode('utf8')

    index = 14 + clientIDlen
    will = None

    if willFlag is not None:
        willtopicNamelenData = data[index:index + 2]
        willtopicNamelenTuple = struct.unpack('h', willtopicNamelenData[::-1])
        willtopicNamelen = willtopicNamelenTuple[0]
        index += 2

        willtopicName = data[index:index + willtopicNamelen].decode('utf8')
        index += willtopicNamelen

        willMessageStrlenData = data[index:index + 1]
        willMessageStrlenTuple = struct.unpack('B', willMessageStrlenData)
        willMessageStrlen = willMessageStrlenTuple[0]
        index += 1

        willMessageStr = data[index:index + willMessageStrlen].decode('utf8')
        index += willMessageStrlen

        if len(willtopicName) == 0:
            raise ValueError('Decode. Connect. Will topic contains invalid will encoding')
        topic = MQTopic(willtopicName, qos)
        will = Will(topic, willMessageStr, willRetainFlag)

        if not will.valid():
            raise ValueError('Decode. Connect. Will contains invalid will encoding')

    username = None
    if userNameFlag == True:
        userNamelenDatalen = data[index:index + 2]
        userNamelenDataTuple = struct.unpack('h', userNamelenDatalen[::-1])
        userNamelenDatalen = userNamelenDataTuple[0]
        index += 2

        username = data[index:index + userNamelenDatalen].decode('utf8')
        index += userNamelenDatalen

    password = None
    if passwordFlag == True:
        passwordlenDatalen = data[index:index + 2]
        passwordlenDataTuple = struct.unpack('h', passwordlenDatalen[::-1])
        passwordlenDatalen = passwordlenDataTuple[0]
        index += 2

        password = data[index:index + passwordlenDatalen].decode('utf8')

    message = MQConnect(username, password, clientID, cleanSessionFlag, keepAlive, will)

    if protocolLevel != 4:
        message.setProtocolLevel = protocolLevel
    return message


def MQ_CONNACK_DECODE(self):
    data = bytearray(self.buffer)

    sessionPresentdata = data[2:3]
    sessionPresent = struct.unpack('B', sessionPresentdata)
    if sessionPresent[0] < 0 | sessionPresent[0] > 1:
        raise ValueError('Decode. Connack. Session-present set to ' + str(sessionPresent[0]))

    connectReturnCodeData = data[3:4]
    connectReturnCode = struct.unpack('B', connectReturnCodeData)

    if MQConnack.isValidReturnCode(connectReturnCode[0]) != True:
        raise ValueError('Decode. Connack. Invalid connack code')

    message = MQConnack(sessionPresent[0], connectReturnCode[0])
    return message


def MQ_PUBLISH_DECODE(self):
    data = bytearray(self.buffer)
    fixedHeaderTuple = struct.unpack('B', data[0:1])
    fixedHeader = fixedHeaderTuple[0]

    dataLengthGet = struct.unpack('h', data[1:3])
    dataLength = dataLengthGet[0]
    # print('dataLength= ' + str(dataLength))
    fixedHeader &= 0xf
    dup = ((fixedHeader >> 3) & 1) == 1

    qos = QoS((fixedHeader & 0x07) >> 1)

    if qos.getValue() == 3:
        raise ValueError('Decode. Publish. Invalid QoS value')
    if (bool(dup) == True) & (qos.getValue() == 0):  # AT_MOST_ONCE
        raise ValueError('Decode. Publish. QoS-0 dup flag present')

    retain = (fixedHeader & 1) == 1

    if dataLength > 255:
        index = 3
    else:
        index = 2

    topicNameData = data[index:index + 2]
    index += 2
    topicNameLenTuple = struct.unpack('h', topicNameData[::-1])
    topicNameLen = topicNameLenTuple[0]
    # print('topicNameLen= ' + str(topicNameLen))
    topicName = data[index:index + topicNameLen].decode(encoding='utf-8')
    # print('topicName= ' + str(topicName))
    packetID = 0

    index += topicNameLen
    if qos.getValue() != 0:
        packetIDdata = data[index:index + 2]
        packetIDTuple = struct.unpack('h', packetIDdata[::-1])
        packetID = packetIDTuple[0]
        if (packetID < 0) | (packetID > 65535):
            raise ValueError('Decode. Publish. Invalid Publish packetID encoding')
        dataLength -= 2
        index += 2

    content = None
    if dataLength > 0:
        content = data[index:index + dataLength].decode('utf8')

    topic = MQTopic(topicName, qos)

    message = MQPublish(packetID, topic, content, bool(retain), bool(dup))
    return message


def MQ_PUBACK_DECODE(self):
    data = bytearray(self.buffer)
    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    message = MQPuback(packetID)
    return message


def MQ_PUBREC_DECODE(self):
    data = bytearray(self.buffer)
    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    message = MQPubrec(packetID)
    return message


def MQ_PUBREL_DECODE(self):
    data = bytearray(self.buffer)
    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    message = MQPubrel(packetID)
    return message


def MQ_PUBCOMP_DECODE(self):
    data = bytearray(self.buffer)
    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    message = MQPubcomp(packetID)
    return message


def MQ_SUBSCRIBE_DECODE(self):
    data = bytearray(self.buffer)

    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    listMQTopics = []
    index = 4
    while index <= len(data) - 1:

        lsbData = data[index:index + 2]
        lsbTuple = struct.unpack('h', lsbData[::-1])
        lsb = lsbTuple[0]

        index += 2

        topicName = data[index:index + lsb].decode('utf8')
        index += lsb

        qosValue = struct.unpack('B', data[index:index + 1])
        qos = QoS(qosValue[0])
        if (qos.getValue() < 0) | (qos.getValue() > 2):
            raise ValueError('Subscribe qos must be in range from 0 to 2:' + str(qos.getValue()))

        topic = MQTopic(topicName, qos)  # type: MQTopic
        listMQTopics.append(topic)
        index += 1

    if len(listMQTopics) == 0:
        raise ValueError('Subscribe with 0 topics')
    message = MQSubscribe(packetID, listMQTopics)
    return message


def MQ_SUBACK_DECODE(self):
    data = bytearray(self.buffer)

    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    listCodes = []
    index = 4
    while index <= len(data) - 1:
        codeTuple = struct.unpack('B', data[index:index + 1])
        code = codeTuple[0]
        if code not in [0, 1, 2, 128]:
            raise ValueError('Invalid suback code: ' + str(code))
        listCodes.append(code)
        index += 1

    message = MQSuback(packetID, listCodes)
    return message


def MQ_UNSUBSCRIBE_DECODE(self):
    data = bytearray(self.buffer)

    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    listTopicNames = []
    index = 4
    while index <= len(data) - 1:
        lsbData = data[index:index + 2]
        lsbTuple = struct.unpack('h', lsbData[::-1])
        lsb = lsbTuple[0]

        index += 2
        topicName = data[index:index + lsb].decode('utf8')

        listTopicNames.append(topicName)
        index += lsb

    if len(listTopicNames) == 0:
        raise ValueError('Unsubscribe with 0 topics')

    message = MQUnsubscribe(packetID, listTopicNames)
    return message


def MQ_UNSUBACK_DECODE(self):
    data = bytearray(self.buffer)

    packetIDdata = data[2:4]
    packetIDTuple = struct.unpack('h', packetIDdata[::-1])
    packetID = packetIDTuple[0]

    message = MQUnsuback(packetID)
    return message


def MQ_PINGREQ_DECODE(self):
    message = MQPingreq()
    return message


def MQ_PINGRESP_DECODE(self):
    message = MQPingresp()
    return message


def MQ_DISCONNECT_DECODE(self):
    message = MQDisconnect()
    return message


switcherDecode = {
    1: MQ_CONNECT_DECODE,
    2: MQ_CONNACK_DECODE,
    3: MQ_PUBLISH_DECODE,
    4: MQ_PUBACK_DECODE,
    5: MQ_PUBREC_DECODE,
    6: MQ_PUBREL_DECODE,
    7: MQ_PUBCOMP_DECODE,
    8: MQ_SUBSCRIBE_DECODE,
    9: MQ_SUBACK_DECODE,
    10: MQ_UNSUBSCRIBE_DECODE,
    11: MQ_UNSUBACK_DECODE,
    12: MQ_PINGREQ_DECODE,
    13: MQ_PINGRESP_DECODE,
    14: MQ_DISCONNECT_DECODE
}


def decode_messageType_method(self, argument):
    return switcherDecode[argument].__call__(self)
