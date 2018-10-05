class CoapMessage(object):
    def __init__(self, version, type, code, messageID, token, options, payload):
        self.version = version
        self.type = type
        self.code = code
        self.messageID = messageID
        self.token = token
        self.options = options
        self.payload = payload

    def equals(self, obj):
        if self == obj:
            return True
        return False

    def getVersion(self):
        return self.version

    def setVersion(self, version):
        self.version = version

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getMessageID(self):
        return self.messageID

    def setMessageID(self, messageID):
        self.messageID = messageID

    def getToken(self):
        return self.token

    def setToken(self, token):
        self.token = token

    def getOptions(self):
        return sorted(self.options, key=lambda CoapOption: CoapOption.type.value)

    def getOptionsDecode(self):
        return self.options

    def setOptions(self, options):
        self.options = options

    def getPayload(self):
        return self.payload

    def setPayload(self, payload):
        self.payload = payload