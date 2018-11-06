from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.avps.AMQPType import *
from venv.iot.amqp.constructor.SimpleConstructor import *
from venv.iot.amqp.tlv.impl.TLVNull import *
from venv.iot.classes.NumericUtil import NumericUtil as util

class TLVMap(TLVAmqp):
    def __init__(self, code, map):
        if code is None or map is None:
            self.width = 1
            self.count = 0
            self.size = 1
            self.map = None
            self.constructor = SimpleConstructor(AMQPType.MAP_8)
        else:
            self.map = map
            if isinstance(code, AMQPType):
                if code == AMQPType.MAP_8:
                    self.width = 1
                else:
                    self.width = 4
            self.size += self.width

            if isinstance(map, dict):
                for key, value in map.items():
                    if isinstance(key, TLVAmqp) and isinstance(value, TLVAmqp):
                        self.size += key.getLength()
                        self.size += value.getLength()

            self.count = len(self.map)
            self.constructor = SimpleConstructor(code)

    def update(self):
        if self.width == 1 and self.size > 255:
            self.constructor.setCode(AMQPType.MAP_32)
            self.width = 4
            self.size += 3

    def putElement(self, key, value):
        if isinstance(self.map, dict):
            self.map[key] = value
        if isinstance(key, TLVAmqp) and isinstance(value, TLVAmqp):
            self.size += key.getLength() + value.getLength()
        self.count += 1
        self.update()

    def getBytes(self):
        constructorBytes = self.constructor.getBytes()

        sizeBytes = bytearray()
        if self.width == 1:
            sizeBytes = util.addByte(sizeBytes, self.size)
        else:
            sizeBytes = util.addInt(sizeBytes, self.size)

        countBytes = bytearray()
        if self.width == 1:
            countBytes = util.addByte(countBytes, self.count*2)
        else:
            countBytes = util.addInt(countBytes, self.count*2)

        valueBytes = bytearray()
        pos = 0
        if isinstance(self.map, dict):
            for key, value in self.map.items():
                if isinstance(key, TLVAmqp) and isinstance(value, TLVAmqp):
                    keyBytes = key.getBytes()
                    valBytes = value.getBytes()
                    valueBytes.append(keyBytes)
                    pos += len(keyBytes)
                    valueBytes.append(valBytes)
                    pos += len(valBytes)

        data = bytearray()
        data.append(constructorBytes)
        if self.size > 0:
            data += sizeBytes
            data += countBytes
            data += valueBytes

        print('TLVMap getBytes ' + str(data))
        return data

    def getMap(self):
        return self.map

    def getValue(self):
        return None

    def getLength(self):
        return self.constructor.getLength() + self.width + self.size

    def getCode(self):
        return self.constructor.getCode()

    def getConstructor(self):
        return self.constructor

    def isNull(self):
        pass

    def setCode(self, arg):
        pass

    def setConstructor(self, arg):
        pass