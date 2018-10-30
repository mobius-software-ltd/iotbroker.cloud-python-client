from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *
from venv.iot.amqp.tlv.api.TLVAmqp import *

class DescribedConstructor(SimpleConstructor):
    def __init__(self, code, descriptor):
        self.code = code
        self.descriptor = descriptor

    def getDescriptor(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor

    def setCode(self, code):
        self.code = code

    def getLength(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor.getLength() + 2

    def getBytes(self):
        data = []
        if isinstance(self.descriptor, TLVAmqp):
            data.append(self.descriptor.getBytes())
            data[0] = 0
            if isinstance(self.code, AMQPType):
                data[len(data)-1] = self.code.value
        return data

    def getDescriptorCode(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor.getBytes()[1]