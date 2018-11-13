import numpy as np
from venv.iot.amqp.wrappers.AMQPMessageFormat import *

x = np.float32(1.0)
if isinstance(x, np.float32):
    print(x.dtype)

listt = [1,2,3]
if isinstance(listt,list):
    print('list ' + str(listt[0]))

d = {'abc':'abc','def':{'ghi':'ghi','jkl':'jkl'}}
for ele in d.values():
    if isinstance(ele,dict):
       for k, v in ele.items():
           print(k,' ',v)

d = {'one':'1','two':'2'}
d['three'] = 3
d.pop('one')
for k, v in d.items():
    print(k, ' ', v)

import uuid
print(str(str(uuid.uuid4())))
print(str(uuid.UUID('4e3d5c02-ab4e-43ab-b082-7b4b131d3c95')))

z = bin(21)
print(type(z))
if isinstance(z,(bytes,bytearray)):
    print('Binary')


rList = [1, 2, 3, 4, 5]

arr = bytes(rList)
print(str(arr[1]))

mf1 = AMQPMessageFormat(125874,10,20)
mf2 = AMQPMessageFormat(None,10,20)

print(str(mf1.getMessageFormat()) + " " + str(mf1.getVersion()))
print(str(mf2.getMessageFormat()) + " " + str(mf2.getVersion()))


c = 4
if c in (1,2,3,4,5):
    print('IS IN')

from venv.iot.amqp.tlv.api.TLVAmqp import *
from venv.iot.amqp.tlv.impl.TLVList import *

list = TLVList(None,None)
if isinstance(list, TLVAmqp):
    print('TLVAmqp')
if isinstance(list, TLVList):
    print('TLVList')

from datetime import datetime
dt = datetime.utcnow()
dt64 = np.datetime64(dt)
ts = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
print(str(ts))

from venv.iot.amqp.avps.AMQPType import *
print(str(AMQPType(0x1D)))

from venv.iot.amqp.state.SASLState import *
from venv.iot.amqp.avps.HeaderCode import *
print(str(SASLState.validate(HeaderCode.MECHANISMS)))
print(str(SASLState.validate(HeaderCode.INIT)))
print(str(SASLState.validate(HeaderCode.OUTCOME)))

from venv.iot.amqp.wrappers.MessageID import *
from venv.iot.amqp.wrappers.LongID import *
long = LongID(10)
if isinstance(long, LongID):
    print('Long')
if isinstance(long, MessageID):
    print('MessageID ' + str(long.getLong()))

print(HeaderCode.TRANSFER.value)

from venv.iot.amqp.constructor.SimpleConstructor import *
constr = SimpleConstructor('123')
print(str(constr.getLength()))

import binascii
print(int(binascii.hexlify(b'AMQP'),16))

x = np.int64(0)
#print(str(x.__class__.__name__))
print('')
if  isinstance(x, np.int64):
    print('int')

