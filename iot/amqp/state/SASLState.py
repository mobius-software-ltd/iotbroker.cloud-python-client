from venv.iot.amqp.avps.HeaderCode import *
from enum import Enum

class SASLState(Enum):
    NONE                = 'NONE'
    MECHANISMS_SENT     = 'MECHANISMS_SENT'
    INIT_RECEIVED       = 'INIT_RECEIVED'
    CHALLENGE_SENT      = 'CHALLENGE_SENT'
    RESPONSE_RECEIVED   = 'RESPONSE_RECEIVED'
    NEGOTIATED          = 'NEGOTIATED'

    @classmethod
    def validate(self, code):
        if isinstance(code, HeaderCode):
            if code == HeaderCode.MECHANISMS:
                return self.NONE
            elif code == HeaderCode.INIT:
                return self.MECHANISMS_SENT
            elif code == HeaderCode.CHALLENGE:
                return self.INIT_RECEIVED
            elif code == HeaderCode.RESPONSE:
                return self.CHALLENGE_SENT
            elif code == HeaderCode.OUTCOME:
                return self.RESPONSE_RECEIVED
            else:
                return self.NEGOTIATED


