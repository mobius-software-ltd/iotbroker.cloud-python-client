class MQConnect(object):
    def __init__(self,username,password,clientID,cleanSession,keepAlive,will):
        self.username = username
        self.password = password
        self.clientID = clientID
        self.cleanSession = cleanSession
        self.keepAlive = keepAlive
        self.will = will
        self.protocolLevel = 4

    def getLength(self):
        length = 10
        length = length + len(self.clientID) + 2
        if self.will is not None:
            length = length + self.will.getLength()

        if self.username is not None:
            length = length + len(self.username) + 2

        if self.password is not None:
            length = length + len(self.password) + 2

        return int(length)

    def getType(self):
        return 1

    def getProtocol(self):
        return 1

    def setProtocolLevel(self, level):
        self.protocolLevel = level

    def willValid(self):
        if self.will.getLength()==0:
            return False
        return True

    def getLengthWill(self):
        return self.will.getLength

    def getKeepAlive(self):
        return self.keepAlive