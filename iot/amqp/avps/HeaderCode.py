from venv.iot.amqp.header.impl.AMQPAttach import *
from venv.iot.amqp.header.impl.AMQPBegin import *
from venv.iot.amqp.header.impl.AMQPClose import *
from venv.iot.amqp.header.impl.AMQPDetach import *
from venv.iot.amqp.header.impl.AMQPDisposition import *
from venv.iot.amqp.header.impl.AMQPEnd import *
from venv.iot.amqp.header.impl.AMQPFlow import *
from venv.iot.amqp.header.impl.AMQPOpen import *
from venv.iot.amqp.header.impl.AMQPTransfer import *
from venv.iot.amqp.header.impl.SASLChallenge import *
from venv.iot.amqp.header.impl.SASLInit import *
from venv.iot.amqp.header.impl.SASLMechanisms import *
from venv.iot.amqp.header.impl.SASLOutcome import *
from venv.iot.amqp.header.impl.SASLResponse import *

from enum import Enum

class HeaderCode(Enum):
    OPEN        = 0x10
    BEGIN       = 0x11
    ATTACH      = 0x12
    FLOW        = 0x13
    TRANSFER    = 0x14
    DISPOSITION = 0x15
    DETACH      = 0x16
    END         = 0x17
    CLOSE       = 0x18
    MECHANISMS  = 0x40
    INIT        = 0x41
    CHALLENGE   = 0x42
    RESPONSE    = 0x43
    OUTCOME     = 0x44
    PING        = 0xff
    PROTO       = 0xfe

    @classmethod
    def emptyHeader(self):
        if self == HeaderCode.ATTACH:
            return AMQPAttach()
        elif self == HeaderCode.BEGIN:
            return AMQPBegin()
        elif self == HeaderCode.CLOSE:
            return AMQPClose()
        elif self == HeaderCode.DETACH:
            return AMQPDetach()
        elif self == HeaderCode.DISPOSITION:
            return AMQPDisposition()
        elif self == HeaderCode.END:
            return AMQPEnd()
        elif self == HeaderCode.FLOW:
            return AMQPFlow()
        elif self == HeaderCode.OPEN:
            return AMQPOpen()
        elif self == HeaderCode.TRANSFER:
            return AMQPTransfer()
        else:
            raise ValueError('Received amqp-header with unrecognized performative')

    @classmethod
    def emptySASL(self):
        if self == HeaderCode.CHALLENGE:
            return SASLChallenge()
        elif self == HeaderCode.INIT:
            return SASLInit()
        elif self == HeaderCode.MECHANISMS:
            return SASLMechanisms()
        elif self == HeaderCode.OUTCOME:
            return SASLOutcome()
        elif self == HeaderCode.RESPONSE:
            return SASLResponse()
        else:
            raise ValueError('Received sasl-header with unrecognized arguments code')