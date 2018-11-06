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
        data = bytearray(1)
        if isinstance(self.descriptor, TLVAmqp):
            descriptorBytes = self.descriptor.getBytes()
            data += descriptorBytes
            #print('DATA ' + str(data) + ' descriptorBytes= ' + str(descriptorBytes))
            if isinstance(self.code, AMQPType):
                data.append(self.code.value)
        #print('DATA ' + str(data))
        return data

    def getDescriptorCode(self):
        if isinstance(self.descriptor, TLVAmqp):
            return self.descriptor.getBytes()[1]