class CoapOption(object):
    def __init__(self, type, length, value):
        self.type = type
        self.length = length
        self.value = value

    def equals(self, obj):
        if self == obj:
            return True
        return False

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value