import struct

class NumericUtil(object):

    def addByte(data, byte):
        data.append(byte)
        return data

    def getByte(data, index):
        tuple = struct.unpack('B', data[index: index + 1])
        return tuple[0]

    def addShort(data, short):
        dataStruct = struct.pack('h', short)
        data += dataStruct[::-1]
        return data

    def getShort(data):
        tuple = struct.unpack('h', data[::-1])
        return tuple[0]

    def addInt(data, int):
        dataStruct = struct.pack('i', int)
        data += dataStruct[::-1]
        return data

    def getInt(data):
        tuple = struct.unpack('i', data[::-1])
        return tuple[0]

    def addLong(data, long):
        dataStruct = struct.pack('q', long)
        data += dataStruct[::-1]
        return data

    def getLong(data):
        tuple = struct.unpack('q', data[::-1])
        return tuple[0]

    def addFloat(data, float):
        dataStruct = struct.pack('f', float)
        data += dataStruct[::-1]
        return data

    def getFloat(data):
        tuple = struct.unpack('f', data[::-1])
        return tuple[0]

    def addDouble(data, double):
        dataStruct = struct.pack('d', double)
        data += dataStruct[::-1]
        return data

    def getDouble(data):
        tuple = struct.unpack('d', data[::-1])
        return tuple[0]

    def addString(dataIn, text):
        data = dataIn
        for ch in text:
            ch = bytes(ch, encoding='utf_8')
            data += struct.pack('c', ch)
        return data

    def getString(data):
        return data.decode('utf_8')