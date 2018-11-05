from venv.iot.amqp.AMQPParser import *

parser = AMQPParser()

header = AMQPProtoHeader(3)
data = parser.encode(header)
print('Encoded data: ' + str(data) + ' AMQPProtoHeader')

header = AMQPPing()
data = parser.encode(header)
print('Encoded data: ' + str(data) + ' AMQPPing')

mechanisms = []
symbol = AMQPSymbol("symbol")
mechanisms.append(symbol)
header = SASLMechanisms(None,None,None,None,mechanisms)
print(header.toString())
data = parser.encode(header)
print('Encoded data: ' + str(data) + ' SASLMechanisms')