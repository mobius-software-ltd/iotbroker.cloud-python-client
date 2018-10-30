from venv.iot.amqp.wrappers.MessageID import *

class BinaryID(MessageID):
    def __init__(self, id):
        self.id = id

    def getString(self):
        return None

    def getBinary(self):
        return self.id

    def getLong(self):
        return None

    def getUuid(self):
        return None