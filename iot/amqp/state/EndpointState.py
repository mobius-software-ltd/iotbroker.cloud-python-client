from enum import Enum

class EndpointState(Enum):
    HDR_RCV     = 'HDR_RCV'
    HDR_SENT    = 'HDR_SENT'
    HDR_EXCH    = 'HDR_EXCH'
    OPEN_PIPE   = 'OPEN_PIPE'
    OC_PIPE     = 'OC_PIPE'
    OPEN_RCVD   = 'OPEN_RCVD'
    OPEN_SENT   = 'OPEN_SENT'
    CLOSE_PIPE  = 'CLOSE_PIPE'
    CLOSE_RCVD  = 'CLOSE_RCVD'
    CLOSE_SENT  = 'CLOSE_SENT'
    DISCARDING  = 'DISCARDING'
    END         = 'END'
    UNMAPPED    = 'UNMAPPED'
    BEGIN_SENT  = 'BEGIN_SENT'
    BEGIN_RCVD  = 'BEGIN_RCVD'
    MAPPED      = 'MAPPED'
    END_SENT    = 'END_SENT'
    END_RCVD    = 'END_RCVD'
    START       = 'START'
    OPENED      = 'OPENED'