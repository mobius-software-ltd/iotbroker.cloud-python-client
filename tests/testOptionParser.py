from iot.coap.options.OptionParser import *

parser = OptionParser()

option = parser.encode(CoapOptionType.ACCEPT, 7)
print('Encoded number= ' + str(option.getType()) + ' length= ' + str(option.getLength()) + ' value=' + str(option.getValue()))
value = parser.decode(CoapOptionType.ACCEPT, option)
print('Decoded value= ' + str(value))

option = parser.encode(CoapOptionType.MAX_AGE, 152)
print('Encoded number= ' + str(option.getType()) + ' length= ' + str(option.getLength()) + ' value=' + str(option.getValue()))
value = parser.decode(CoapOptionType.MAX_AGE, option)
print('Decoded value= ' + str(value))

option = parser.encode(CoapOptionType.IF_MATCH, 'ifmatch')
print('Encoded number= ' + str(option.getType()) + ' length= ' + str(option.getLength()) + ' value=' + str(option.getValue()))
value = parser.decode(CoapOptionType.IF_MATCH, option)
print('Decoded value= ' + str(value))