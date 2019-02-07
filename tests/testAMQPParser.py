from iot.amqp.AMQPParser import *

parser = AMQPParser()

header = AMQPProtoHeader(3)
print('Input header   ' + header.toString())
data = parser.encode(header)
print('Encoded data: ' + str(data) + ' AMQPProtoHeader')
headerDecoded = parser.decode(data)
print('Decoded header ' + headerDecoded.toString())

print('____________________________________________________________')
header = AMQPPing()
print('Input header   ' + header.toString())
data = parser.encode(header)
print('Encoded data: ' + str(data) + ' AMQPPing')
headerDecoded = parser.decode(data)
print('Decoded header ' + headerDecoded.toString())

print('____________________________________________________________')
mechanisms = []
symbol = AMQPSymbol("PLAIN")
mechanisms.append(symbol)
header = SASLMechanisms(None,None,None,None,mechanisms)
print('Input header   ' + header.toString())
data = parser.encode(header)
print('Encoded data: ' + str(data) + ' SASLMechanisms')
headerDecoded = parser.decode(data)
print('Decoded header ' + headerDecoded.toString())
