from venv.iot.classes.NumericUtil import NumericUtil as util

class AMQPMessageFormat(object):
    def __init__(self, value, messageFormat, version):
        if value != None:
            self.initValue(value)
        else:
            self.initFormat(messageFormat, version)

    def initValue(self, value):
        arr = bytearray()
        arr = util.addInt(arr, value)
        mf = bytearray(4)
        mf[1:3] = arr[0:2]
        self.messageFormat = util.getInt(mf)
        self.version = arr[3] & 0xff

    def initFormat(self, messageFormat, version):
        self.messageFormat = messageFormat
        self.version = version

    def getMessageFormat(self):
        return self.messageFormat

    def getVersion(self):
        return self.version

    def encode(self):
        arr = bytearray(3)
        mf = bytearray(4)
        mf = util.addInt(mf, self.getMessageFormat())
        arr[0:2] = mf[1:3]
        arr = util.addByte(arr,self.getVersion())
        return util.getLong(arr)



