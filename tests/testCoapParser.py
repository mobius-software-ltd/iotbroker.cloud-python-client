from iot.coap.CoapParser import *
from iot.coap.tlv.CoapType import *
from iot.coap.tlv.CoapCode import *

from iot.coap.options.OptionParser import *

parserOption = OptionParser()
parser = CoapParser()

option1 = parserOption.encode(CoapOptionType.ACCEPT, 7)
option2 = parserOption.encode(CoapOptionType.MAX_AGE, 152)
option3 = parserOption.encode(CoapOptionType.IF_MATCH, 'ifmatch')

options = []
options.append(option1)
print('option1 type ' + str(option1.getType()))
options.append(option2)
options.append(option3)
print('options ' + str(options))
message = CoapMessage(1,CoapType.CONFIRMABLE,CoapCode.CHANGED,7,'token',options,'payload')
data = parser.encode(message)
print('Encoded ' + str(data))

messageDecoded = parser.decode(data)
print('Decoded ' + str(messageDecoded))
if isinstance(messageDecoded, CoapMessage):
    print('version: ' + str(messageDecoded.getVersion()))
    print('type: ' + str(messageDecoded.getType()))
    print('code: ' + str(messageDecoded.getCode()))
    print('messageID: ' + str(messageDecoded.getPacketID()))
    print('token: ' + str(messageDecoded.getToken()))
    print('payload: ' + str(messageDecoded.getPayload()))
    print('options:')
    for option in messageDecoded.getOptionsDecode():
        if isinstance(option, CoapOption):
            print('----------------')
            print('option type: ' + str(CoapOptionType(option.getType())))
            print('option value: ' + str(parserOption.decode(CoapOptionType(option.getType()),option)))
            print('----------------')
