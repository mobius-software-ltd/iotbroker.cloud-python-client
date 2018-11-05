from venv.iot.amqp.constructor.SimpleConstructor import *
from venv.iot.amqp.avps.AMQPType import *
import abc

class TLVAmqp(metaclass=abc.ABCMeta):
    def __init__(self, constructor):
        self.constructor = constructor

    @abc.abstractmethod
    def getConstructor(self):
        return self.constructor

    @abc.abstractmethod
    def setConstructor(self, arg):
        self.constructor = arg

    @abc.abstractmethod
    def getCode(self):
        if isinstance(self.constructor, SimpleConstructor):
            return self.constructor.getCode()

    @abc.abstractmethod
    def setCode(self, arg):
        if isinstance(self.constructor, SimpleConstructor):
            self.constructor.setCode(arg)

    @abc.abstractmethod
    def getBytes(self):
        pass

    @abc.abstractmethod
    def getLength(self):
        pass

    @abc.abstractmethod
    def getValue(self):
        pass

    @abc.abstractmethod
    def isNull(self):
        if isinstance(self.constructor, SimpleConstructor):
            if self.constructor.getCode() == AMQPType.NULL:
                return True
            else:
                return False
