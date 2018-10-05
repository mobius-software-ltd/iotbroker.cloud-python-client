from venv.iot.coap.CoapParser import *
from venv.iot.coap.tlv.CoapType import *
from venv.iot.coap.tlv.CoapCode import *

from venv.iot.coap.options.OptionParser import *

parserOption = OptionParser()
parser = CoapParser()

option1 = parserOption.encode(CoapOptionType.ACCEPT, 7)
option2 = parserOption.encode(CoapOptionType.MAX_AGE, 152)
option3 = parserOption.encode(CoapOptionType.IF_MATCH, 'ifmatch')

options = []
options.append(option1)
options.append(option2)
options.append(option3)
message = CoapMessage(1,CoapType.CONFIRMABLE,CoapCode.CHANGED,7,'token',options,'payload')
data = parser.encode(message)
print('Encoded ' + str(data))

messageDecoded = parser.decode(data)
print('Decoded ' + str(messageDecoded))
if isinstance(messageDecoded, CoapMessage):
    print('version: ' + str(messageDecoded.getVersion()))
    print('type: ' + str(messageDecoded.getType()))
    print('code: ' + str(messageDecoded.getCode()))
    print('messageID: ' + str(messageDecoded.getMessageID()))
    print('token: ' + str(messageDecoded.getToken()))
    print('payload: ' + str(messageDecoded.getPayload()))
    print('options:')
    for option in messageDecoded.getOptionsDecode():
        if isinstance(option, CoapOption):
            print('----------------')
            print('option type: ' + str(CoapOptionType(option.getType())))
            print('option value: ' + str(parserOption.decode(CoapOptionType(option.getType()),option)))
            print('----------------')
