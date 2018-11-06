from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.HeaderCode import *
from venv.iot.amqp.avps.SectionCode import *
from venv.iot.amqp.avps.StateCode import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVArray import *
from venv.iot.amqp.tlv.impl.TLVList import *
from venv.iot.amqp.tlv.impl.TLVMap import *
from venv.iot.amqp.tlv.impl.TLVFixed import *
from venv.iot.amqp.tlv.impl.TLVVariable import *
from venv.iot.amqp.tlv.impl.AMQPAccepted import *
from venv.iot.amqp.tlv.impl.AMQPModified import *
from venv.iot.amqp.tlv.impl.AMQPReceived import *
from venv.iot.amqp.tlv.impl.AMQPRejected import *
from venv.iot.amqp.tlv.impl.AMQPReleased import *
from venv.iot.amqp.tlv.api.TLVFactory import *
from venv.iot.amqp.header.api.AMQPHeader import *
from venv.iot.amqp.sections.ApplicationProperties import *
from venv.iot.amqp.sections.AMQPData import *
from venv.iot.amqp.sections.DeliveryAnnotations import *
from venv.iot.amqp.sections.AMQPFooter import *
from venv.iot.amqp.sections.MessageHeader import *
from venv.iot.amqp.sections.MessageAnnotations import *
from venv.iot.amqp.sections.AMQPProperties import *
from venv.iot.amqp.sections.AMQPSequence import *
from venv.iot.amqp.sections.AMQPValue import *
from venv.iot.amqp.header.impl.SASLMechanisms import *
from venv.iot.amqp.header.impl.SASLChallenge import *
from venv.iot.amqp.header.impl.SASLInit import *
from venv.iot.amqp.header.impl.SASLOutcome import *
from venv.iot.amqp.header.impl.SASLResponse import *

class HeaderFactory(object):
    def __init__(self, index):
        self.index = index
        self.tlvFactory = TLVFactory(index)

    def getIndex(self):
        return self.index

    def setIndex(self,index):
        self.index = index

    def getAMQP(self, buf):
        list = self.tlvFactory.getTlv(buf)
        self.index = self.tlvFactory.getIndex()

        if list is not None and isinstance(list,TLVAmqp):
            code  = list.getCode()
            if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                raise ValueError('Received amqp-header with malformed arguments')

            byteCode = list.getConstructor().getDescriptorCode()
            code = HeaderCodeClear(byteCode)

            if code == HeaderCodeClear.ATTACH:
                header = AMQPAttach()
            elif code == HeaderCodeClear.BEGIN:
                header = AMQPBegin()
            elif code == HeaderCodeClear.CLOSE:
                header = AMQPClose()
            elif code == HeaderCodeClear.DETACH:
                header = AMQPDetach()
            elif code == HeaderCodeClear.DISPOSITION:
                header = AMQPDisposition()
            elif code == HeaderCodeClear.END:
                header = AMQPEnd()
            elif code == HeaderCodeClear.FLOW:
                header = AMQPFlow()
            elif code == HeaderCodeClear.OPEN:
                header = AMQPOpen()
            elif code == HeaderCodeClear.TRANSFER:
                header = AMQPTransfer()

            if isinstance(header, AMQPHeader):
                header.fromArgumentsList(list)
                return header
        return None

    def getSASL(self, buf):
        #print('getSASL ' + str(buf) + ' ' +str(self.index))
        list = self.tlvFactory.getTlv(buf)
        #print('EXIT')
        self.index = self.tlvFactory.getIndex()
        #print('list ' + str(self.index))
        if list is not None and isinstance(list,TLVAmqp):

            code  = list.getCode()
            if code not in (AMQPType.LIST_0,AMQPType.LIST_8,AMQPType.LIST_32):
                raise ValueError('Received sasl-header with malformed arguments')

            byteCode = list.getConstructor().getDescriptorCode()
            #print('list.getConstructor() ' + str(list.getValue()))
            code = HeaderCode(byteCode)
            #print('code ' + str(code))

            #header = HeaderCode.emptySASL()
            if code == HeaderCode.CHALLENGE:
                header = SASLChallenge(None,None,None,None,None)
            elif code == HeaderCode.INIT:
                header = SASLInit(None,None,None,None,None,None,None)
            elif code == HeaderCode.MECHANISMS:
                header = SASLMechanisms(None,None,None,None,None)
            elif code == HeaderCode.OUTCOME:
                header = SASLOutcome(None,None,None,None,None,None)
            elif code == HeaderCode.RESPONSE:
                header = SASLResponse(None,None,None,None,None)

            if isinstance(header, AMQPHeader):
                header.fromArgumentsList(list)
                return header

    def getSection(self, buf):
        value = self.tlvFactory.getTlv(buf)
        self.index = self.tlvFactory.getIndex()
        section = None
        byteCode = value.getConstructor().getDescriptorCode()
        code = SectionCode(byteCode)
        if code == SectionCode.APPLICATION_PROPERTIES:
            section = ApplicationProperties(None)
        elif code == SectionCode.DATA:
            section = AMQPData(None)
        elif code == SectionCode.DELIVERY_ANNOTATIONS:
            section = DeliveryAnnotations(None)
        elif code == SectionCode.FOOTER:
            section = AMQPFooter(None)
        elif code == SectionCode.HEADER:
            section = MessageHeader(None)
        elif code == SectionCode.MESSAGE_ANNOTATIONS:
            section = MessageAnnotations(None)
        elif code == SectionCode.PROPERTIES:
            section = AMQPProperties(None)
        elif code == SectionCode.SEQUENCE:
            section = AMQPSequence(None)
        elif code == SectionCode.VALUE:
            section = AMQPValue(None)
        else:
            raise ValueError('Received header with unrecognized message section code')
        if section is not None:
            section.fill(value)
            return section

    def getState(self, list):
        state = None
        if isinstance(list, TLVList):
            byteCode = list.getConstructor().getDescriptorCode()
            code = StateCode(byteCode)
            if code == StateCode.ACCEPTED:
                state = AMQPAccepted()
            elif code == StateCode.MODIFIED:
                state = AMQPModified(None,None,None)
            elif code == StateCode.RECEIVED:
                state = AMQPReceived(None,None)
            elif code == StateCode.REJECTED:
                state = AMQPRejected(None)
            elif code == StateCode.RELEASED:
                state = AMQPReleased()
            else:
                raise ValueError('Received header with unrecognized state code')
        return state

    def getOutcome(self, list):
        outcome = None
        if isinstance(list, TLVList):
            byteCode = list.getConstructor().getDescriptorCode()
            code = StateCode(byteCode)
            if code == StateCode.ACCEPTED:
                outcome = AMQPAccepted()
            elif code == StateCode.MODIFIED:
                outcome = AMQPModified(None,None,None)
            elif code == StateCode.REJECTED:
                outcome = AMQPRejected(None)
            elif code == StateCode.RELEASED:
                outcome = AMQPReleased()
            else:
                raise ValueError('Received header with unrecognized outcome code')
        return outcome