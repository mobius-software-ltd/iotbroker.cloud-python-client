from enum import Enum

class TerminusExpiryPolicy(Enum):
    LINK_DETACH     = "link-detach"
    SESSION_END     = "session-end"
    CONNETION_CLOSE = "connection-close"
    NEVER           = "never"
