from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.avps.ErrorCode import *
from venv.iot.amqp.constructor.DescribedConstructor import *
from venv.iot.amqp.header.api.AMQPUnwrapper import *
from venv.iot.amqp.header.api.AMQPWrapper import *
from venv.iot.amqp.header.api.Parsable import *
from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.wrappers.AMQPSymbol import *

class AMQPModified(Parsable):
    def __init__(self, deliveryFailed, undeliverableHere, messageAnnotations):
        self.deliveryFailed = deliveryFailed
        self.undeliverableHere = undeliverableHere
        self.messageAnnotations = messageAnnotations

    def toArgumentsList(self):
        list = TLVList(None,None)
        if self.deliveryFailed is not None:
            list.addElement(0, AMQPWrapper.wrap(self.deliveryFailed))
        if self.undeliverableHere is not None:
            list.addElement(1, AMQPWrapper.wrap(self.undeliverableHere))
        if self.messageAnnotations is not None and isinstance(self.messageAnnotations,dict):
            if len(self.messageAnnotations) > 0:
                list.addElement(2, AMQPWrapper.wrapMap(self.messageAnnotations))

        constructor = DescribedConstructor(list.getCode(),TLVFixed(AMQPType.SMALL_ULONG, 0x27))
        list.setConstructor(constructor)
        return list

    def fromArgumentsList(self, list):
        if isinstance(list, TLVList):
            if len(list.getList()) > 0 :
                element = list.getList()[0]
                if element is not None:
                    self.deliveryFailed = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 1 :
                element = list.getList()[1]
                if element is not None:
                    self.undeliverableHere = AMQPUnwrapper.unwrapBool(element)
            if len(list.getList()) > 2 :
                element = list.getList()[2]
                if element is not None:
                    self.messageAnnotations = AMQPUnwrapper.unwrapMap(element)

    def toString(self):
        return 'AMQPError [condition='+ str(self.condition) + ', description=' + str(self.description) + ', info=' + str(self.info) + ']'

    def getDeliveryFailed(self):
        return self.deliveryFailed

    def setDeliveryFailed(self, deliveryFailed):
        self.deliveryFailed = deliveryFailed

    def getUndeliverableHere(self):
        return self.undeliverableHere

    def setUndeliverableHere(self, undeliverableHere):
        self.undeliverableHere = undeliverableHere

    def getMessageAnnotations(self):
        return self.messageAnnotations

    def setMessageAnnotations(self, messageAnnotations):
        self.messageAnnotations = messageAnnotations