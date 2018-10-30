from venv.iot.amqp.wrappers.MessageID import *

class StringID(MessageID):
    def __init__(self, id):
        self.id = id

    def getString(self):
        return self.id

    def getBinary(self):
        return None

    def getLong(self):
        return None

    def getUuid(self):
        return None