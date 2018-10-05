class MQSuback(object):
    def __init__(self,packetID,listCodes):
        self.packetID = packetID
        self.listCodes = listCodes

    def getLength(self):
        return (len(self.listCodes) + 2)

    def getType(self):
        return 9

    def getProtocol(self):
        return 1

    def isValidCode(self, code):
        if code == 0 | code == 1 | code == 2:
            return True
        return False