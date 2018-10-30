from venv.iot.amqp.wrappers.MessageID import *

class LongID(MessageID):
    def __init__(self, id):
        self.id = id

    def getString(self):
        return None

    def getBinary(self):
        return None

    def getLong(self):
        return self.id

    def getUuid(self):
        return None