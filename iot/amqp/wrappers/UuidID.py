from venv.iot.amqp.wrappers.MessageID import *

class UuidID(MessageID):
    def __init__(self, id):
        self.id = id

    def getString(self):
        return None

    def getBinary(self):
        return None

    def getLong(self):
        return None

    def getUuid(self):
        return self.id