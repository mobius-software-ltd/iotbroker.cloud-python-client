from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.ErrorCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.wrappers.AMQPSymbol import *

class AMQPError(Parsable):
    def __init__(self, condition, description, info):
        self.condition = condition
        self.description = description
        self.info = info

    def toArgumentsList(self):
        list = TLVList(None,None)
        if self.condition is not None and isinstance(self.condition, ErrorCode):
            list.addElement(0, AMQPWrapper.wrap(AMQPSymbol(self.condition)))
        if self.description is not None:
            list.addElement(1, AMQPWrapper.wrap(self.description))
        if self.info is not None:
            list.addElement(2, AMQPWrapper.wrap(self.info))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x1D))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None:
                    self.condition = ErrorCode(AMQPUnwrapper.unwrapSymbol(element).getValue())
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None:
                    self.description = AMQPUnwrapper.unwrapString(element)
            if len(list.getList()) > 2 :
                element = list.getList()[2]
                if element is not None:
                    self.info = AMQPUnwrapper.unwrapMap(element)

    def toString(self):
        return 'AMQPError [condition='+ str(self.condition) + ', description=' + str(self.description) + ', info=' + str(self.info) + ']'

    def getCondition(self):
        return self.condition

    def setCondition(self, condition):
        self.condition = condition

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getInfo(self):
        return self.info

    def setInfo(self, info):
        self.info = info