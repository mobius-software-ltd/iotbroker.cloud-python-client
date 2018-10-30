import numpy as np
from venv.iot.amqp.wrappers.AMQPMessageFormat import *

x = np.float32(1.0)
if isinstance(x, np.float32):
    print(x.dtype)

listt = [1,2,3]
if isinstance(listt,list):
    print('list')

d = {'abc':'abc','def':{'ghi':'ghi','jkl':'jkl'}}
for ele in d.values():
    if isinstance(ele,dict):
       for k, v in ele.items():
           print(k,' ',v)

d = {'one':'1','two':'2'}
d['three'] = 3
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

