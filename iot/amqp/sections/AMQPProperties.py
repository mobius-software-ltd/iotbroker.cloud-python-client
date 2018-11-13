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
from venv.iot.amqp.sections.AMQPSection import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.avps.SectionCode import *
from venv.iot.amqp.wrappers.MessageID import *
from venv.iot.amqp.wrappers.LongID import *
from venv.iot.amqp.wrappers.StringID import *
from venv.iot.amqp.wrappers.BinaryID import *
from venv.iot.amqp.wrappers.UuidID import *

class AMQPProperties(AMQPSection):
    def __init__(self,messageId,userId,to,subject,replyTo,correlationId,contentType,contentEncoding,absoluteExpiryTime,creationTime,groupId,groupSequence,replyToGroupId):
        self.messageId = messageId
        self.userId = userId
        self.to = to
        self.subject = subject
        self.replyTo = replyTo
        self.correlationId = correlationId
        self.contentType = contentType
        self.contentEncoding = contentEncoding
        self.absoluteExpiryTime = absoluteExpiryTime
        self.creationTime = creationTime
        self.groupId = groupId
        self.groupSequence = groupSequence
        self.replyToGroupId = replyToGroupId

    def getValue(self):
        list  = TLVList(None, None)

        if self.messageId is not None and isinstance(self.messageId, MessageID):
            value = None
            if self.messageId.getBinary() is not None:
                value = self.messageId.getBinary()
            elif self.messageId.getLong() is not None:
                value = self.messageId.getLong()
            elif self.messageId.getString() is not None:
                value = self.messageId.getString()
            elif self.messageId.getUuid() is not None:
                value = self.messageId.getUuid()
            list.addElement(0, AMQPWrapper.wrap(value))

        if self.userId is not None:
            list.addElement(1, AMQPWrapper.wrap(self.userId))
        if self.to is not None:
            list.addElement(2, AMQPWrapper.wrap(self.to))
        if self.subject is not None:
            list.addElement(3, AMQPWrapper.wrap(self.subject))
        if self.replyTo is not None:
            list.addElement(4, AMQPWrapper.wrap(self.replyTo))
        if self.correlationId is not None:
            list.addElement(5, AMQPWrapper.wrap(self.correlationId))
        if self.contentType is not None:
            list.addElement(6, AMQPWrapper.wrap(self.contentType))
        if self.contentEncoding is not None:
            list.addElement(7, AMQPWrapper.wrap(self.contentEncoding))
        if self.absoluteExpiryTime is not None:
            list.addElement(8, AMQPWrapper.wrap(self.absoluteExpiryTime))
        if self.creationTime is not None:
            list.addElement(9, AMQPWrapper.wrap(self.creationTime))
        if self.groupId is not None:
            list.addElement(10, AMQPWrapper.wrap(self.groupId))
        if self.groupSequence is not None:
            list.addElement(11, AMQPWrapper.wrap(self.groupSequence))
        if self.replyToGroupId is not None:
            list.addElement(12, AMQPWrapper.wrap(self.replyToGroupId))

        constructor = DescribedConstructor(list.getCode(), TLVFixed(AMQPType.SMALL_ULONG, 0x73))
        list.setConstructor(constructor)
        return list

    def fill(self, value):
        list = value
        if isinstance(list, TLVList):
            if len(list.getList()) > 0:
                element = list.getList()[0]
                if element is not None and isinstance(element, TLVAmqp):
                    code = element.getCode()
                    if code in (AMQPType.ULONG_0,AMQPType.SMALL_ULONG,AMQPType.ULONG):
                        self.messageId = LongID(AMQPUnwrapper.unwrapULong(element))
                    elif code in (AMQPType.STRING_8,AMQPType.STRING_32):
                        self.messageId = StringID(AMQPUnwrapper.unwrapString(element))
                    elif code in (AMQPType.BINARY_8,AMQPType.BINARY_32):
                        self.messageId = BinaryID(AMQPUnwrapper.unwrapBinary(element))
                    elif code in (AMQPType.UUID):
                        self.messageId = BinaryID(AMQPUnwrapper.unwrapUuid(element))
                    else:
                        raise ValueError('Expected type MessageID received ' + str(element.getCode()))

            if len(list.getList()) > 1:
                element = list.getList()[1]
                if element is not None:
                    self.userId = AMQPUnwrapper.unwrapBinary(element)
            if len(list.getList()) > 2:
                element = list.getList()[2]
                if element is not None:
                    self.to = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 3:
                element = list.getList()[3]
                if element is not None:
                    self.subject = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 4:
                element = list.getList()[4]
                if element is not None:
                    self.replyTo = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 5:
                element = list.getList()[5]
                if element is not None:
                    self.correlationId = AMQPUnwrapper.unwrapBinary(element)
            if len(list.getList()) > 6:
                element = list.getList()[6]
                if element is not None:
                    self.contentType = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 7:
                element = list.getList()[7]
                if element is not None:
                    self.contentEncoding = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 8:
                element = list.getList()[8]
                if element is not None:
                    self.absoluteExpiryTime = AMQPUnwrapper.unwrapTimastamp(element)
            if len(list.getList()) > 9:
                element = list.getList()[9]
                if element is not None:
                    self.creationTime = AMQPUnwrapper.unwrapTimastamp(element)
            if len(list.getList()) > 10:
                element = list.getList()[10]
                if element is not None:
                    self.groupId = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 11:
                element = list.getList()[11]
                if element is not None:
                    self.groupSequence = AMQPUnwrapper.unwrapUInt(element)
            if len(list.getList()) > 12:
                element = list.getList()[12]
                if element is not None:
                    self.replyToGroupId = AMQPUnwrapper.unwrapString(element)

    def getCode(self):
        return SectionCode.PROPERTIES

    def toString(self):
        return 'AMQPProperties [messageId=' + self.messageId + ', userId=' + self.userId + ', to=' + self.to + ', subject=' + self.subject + ', replyTo=' + self.replyTo + ', correlationId=' + self.correlationId + ', contentType=' + self.contentType + ', contentEncoding=' + self.contentEncoding + ', absoluteExpiryTime=' + self.absoluteExpiryTime + ', creationTime=' + self.creationTime + ', groupId=' + self.groupId + ', groupSequence=' + self.groupSequence + ', replyToGroupId=' + self.replyToGroupId + ']'

    def getMessageId(self):
        return self.messageId

    def setMessageId(self, messageId):
        self.messageId = messageId

    def getUserId(self):
        return self.userId

    def setUserId(self, userId):
        self.userId = userId

    def getTo(self):
        return self.to

    def setTo(self, to):
        self.to = to

    def getSubject(self):
        return self.subject

    def setSubject(self, subject):
        self.subject = subject

    def getReplyTo(self):
        return self.replyTo

    def setReplyTo(self, replyTo):
        self.replyTo = replyTo

    def getCorrelationId(self):
        return self.correlationId

    def setCorrelationId(self, correlationId):
        self.correlationId = correlationId

    def getContentType(self):
        return self.contentType

    def setContentType(self, contentType):
        self.contentType = contentType

    def getContentEncoding(self):
        return self.contentEncoding

    def setContentEncoding(self, contentEncoding):
        self.contentEncoding = contentEncoding

    def getAbsoluteExpiryTime(self):
        return self.absoluteExpiryTime

    def setAbsoluteExpiryTime(self, absoluteExpiryTime):
        self.absoluteExpiryTime = absoluteExpiryTime

    def getCreationTime(self):
        return self.creationTime

    def setCreationTime(self, creationTime):
        self.creationTime = creationTime

    def getGroupId(self):
        return self.groupId

    def setGroupId(self, groupId):
        self.groupId = groupId

    def getGroupSequence(self):
        return self.groupSequence

    def setGroupSequence(self, groupSequence):
        self.groupSequence = groupSequence

    def getReplyToGroupId(self):
        return self.replyToGroupId

    def setReplyToGroupId(self, replyToGroupId):
        self.replyToGroupId = replyToGroupId