from threading import Timer
from venv.IoT.Classes.ConnectionState import *
from venv.IoT.MQTT.MQTTMessages.MQPublish import *

class TimerTask():
    def __init__(self, message, period, client):
        self.message = message
        self.period = period
        self.timer = Timer(self.period, self.handle_function)
        self.status = None
        self.isTimeoutTask = False
        self.client = client
        self.client.send(self.message)

    def handle_function(self):
        self.onTimedEvent()
        self.timer = Timer(self.period, self.handle_function)
        self.timer.start()

    def getPeriod(self):
        return self.period

    def getMessage(self):
        return self.message

    def setIsTimeoutTask(self, value):
        self.isTimeoutTask = value

    def start(self):
        self.timer.start()

    def onTimedEvent(self):
        #print('HERE type ' + str(self.message.getType()) + ' self.isTimeoutTask= ' + str(self.isTimeoutTask))

        if self.isTimeoutTask == True:
            self.client.timeoutMethod()

        if self.client.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            if self.status == True:
                if isinstance(self.message, MQPublish):
                    self.message.dup = True

            self.client.send(self.message)
            self.status = True

    def stop(self):
        self.timer.cancel()