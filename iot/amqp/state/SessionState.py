from enum import Enum

class SessionState(Enum):
    UNMAPPED    = 'UNMAPPED'
    BEGIN_SENT  = 'BEGIN_SENT'
    BEGIN_RCVD  = 'BEGIN_RCVD'
    MAPPED      = 'MAPPED'
    END_SENT    = 'END_SENT'
    END_RCVD    = 'END_RCVD'
    DISCARDING  = 'DISCARDING'