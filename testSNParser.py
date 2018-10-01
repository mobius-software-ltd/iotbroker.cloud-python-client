from venv.IoT.MQTTSN.MQTTSN_messages.Advertise import *
from venv.IoT.MQTTSN.MQTTSN_messages.Encapsulated import *
from venv.IoT.MQTTSN.MQTTSN_messages.GWInfo import *
from venv.IoT.MQTTSN.MQTTSN_messages.Regack import *
from venv.IoT.MQTTSN.MQTTSN_messages.Register import *
from venv.IoT.MQTTSN.MQTTSN_messages.SearchGW import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNConnack import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNConnect import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNDisconnect import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPingreq import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPingresp import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPuback import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPubcomp import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNUnsuback import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPublish import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPubrec import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNPubrel import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNSuback import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNSubscribe import *
from venv.IoT.MQTTSN.MQTTSN_messages.SNUnsubscribe import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillMsg import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillMsgReq import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillMsgResp import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillMsgUpd import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillTopic import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillTopicReq import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillTopicResp import *
from venv.IoT.MQTTSN.MQTTSN_messages.WillTopicUpd import *

from venv.IoT.MQTTSN.SNParser import *

parser = SNParser(None)

#ADVERTISE
gwID = 5
duration = 100
message = Advertise(gwID,duration)
parser.setMessage(message)
data = parser.encode()
print('Advertise')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, Advertise):
    if messageDecoded.getgwID() == gwID and messageDecoded.getDuration() == duration:
        print('Advertise is Ok')
    else:
        print('Advertise Error occured')

print('_____________________________________')
#SEARCHGW
radius = 10
message = SearchGW(radius)
parser.setMessage(message)
data = parser.encode()
print('SearchGW')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SearchGW):
    if messageDecoded.getRadius() == radius:
        print('SearchGW is Ok')
    else:
        print('SearchGW Error occured')

print('_____________________________________')
#GWInfo
gwID = 5
gwAddress = 'localhost'
message = GWInfo(gwID, gwAddress)
parser.setMessage(message)
data = parser.encode()
print('GWInfo')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, GWInfo):
    if messageDecoded.getgwID() == gwID and messageDecoded.getgwAddress() == gwAddress:
        print('GWInfo is Ok')
    else:
        print('GWInfo Error occured')
        print('GWInfo gwID= ' + str(messageDecoded.getgwID()) + ',gwAddress= ' +  str(messageDecoded.getgwAddress()))

print('_____________________________________')
#SNConnect
willPresent = True
cleanSession = False
duration = 128
clientID = 'testID'
message = SNConnect(willPresent, cleanSession, duration, clientID)
parser.setMessage(message)
data = parser.encode()
print('SNConnect')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNConnect):
    if messageDecoded.getWillPresent() == willPresent and messageDecoded.getCleanSession() == cleanSession and messageDecoded.getDuration() == duration and messageDecoded.getClientID() == clientID:
        print('SNConnect is Ok')
    else:
        print('SNConnect Error occured')

print('_____________________________________')
#SNConnack
code = ReturnCode.ACCEPTED.value[0]
message = SNConnack(code)
parser.setMessage(message)
data = parser.encode()
print('SNConnack')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNConnack):
    if messageDecoded.getCode() == code:
        print('SNConnack is Ok')
    else:
        print('SNConnack Error occured')

print('_____________________________________')
#WillTopic
retain = True
qos = QoS(0)
value = 'jdfnkjgn'
topic = FullTopic(value, qos)
message = WillTopic(retain, topic)
parser.setMessage(message)
data = parser.encode()
print('WillTopic')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, WillTopic):
    topic = messageDecoded.getTopic()
    if isinstance(topic, FullTopic):
        if topic.value == value and topic.getQoS() == qos.getValue():
            print('WillTopic is Ok')
        else:
            print('WillTopic Error occured error fields')
    else:
        print('WillTopic Error occured. it is not fullTopic')

print('_____________________________________')
#WillMsg
content = 'textfield'
message = WillMsg(content)
parser.setMessage(message)
data = parser.encode()
print('WillMsg')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, WillMsg):
    if messageDecoded.getContent() == content:
        print('WillMsg is Ok')
    else:
        print('WillMsg Error occured')

print('_____________________________________')
#Register
topicID = 5
messageID = 12
topicName = 'textfieldName'
message = Register(topicID, messageID, topicName)
parser.setMessage(message)
data = parser.encode()
print('Register')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, Register):
    if messageDecoded.getTopicID() == topicID and messageDecoded.getMessageID() == messageID and messageDecoded.getTopicName() == topicName:
        print('Register is Ok')
    else:
        print('Register Error occured')

print('_____________________________________')
#Regack
topicID = 5
messageID = 12
code = ReturnCode.INVALID_TOPIC_ID.value[0]
message = Regack(topicID, messageID, code)
parser.setMessage(message)
data = parser.encode()
print('Regack')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, Regack):
    if messageDecoded.getTopicID() == topicID and messageDecoded.getMessageID() == messageID and messageDecoded.getCode() == code:
        print('Regack is Ok')
    else:
        print('Regack Error occured')       

print('_____________________________________')
#SNPublish
messageID = 12
qos = QoS(2)
value = 'shortName'
topic = ShortTopic(value, qos)
content = 'testContent'
dup = True
retain = False
message = SNPublish(messageID,topic,content,dup,retain)
parser.setMessage(message)
data = parser.encode()
print('SNPublish')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNPublish):
    topic = messageDecoded.getTopic()
    if isinstance(topic, ShortTopic):
        if topic.value == value and topic.getQoS() == qos.getValue() and messageDecoded.isDup() == dup and messageDecoded.isRetain() == retain and messageDecoded.getContent() == content:
            print('SNPublish is Ok')
        else:
            print('SNPublish Error occured error fields')
    else:
        print('SNPublish Error occured. it is not ShortTopic')

print('_____________________________________')
#SNPuback
topicID = 45
messageID = 5
code = ReturnCode.INVALID_TOPIC_ID.value[0]
message = SNPuback(topicID, messageID, code)
parser.setMessage(message)
data = parser.encode()
print('SNPuback')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNPuback):
    if messageDecoded.getTopicID() == topicID and messageDecoded.getMessageID() == messageID and messageDecoded.getCode() == code:
        print('SNPuback is Ok')
    else:
        print('SNPuback Error occured')

print('_____________________________________')
#SNPubcomp
messageID = 5
message = SNPubcomp(messageID)
parser.setMessage(message)
data = parser.encode()
print('SNPubcomp')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNPubcomp):
    if messageDecoded.getMessageID() == messageID:
        print('SNPubcomp is Ok')
    else:
        print('SNPubcomp Error occured')

print('_____________________________________')
#SNPubrec
messageID = 5
message = SNPubrec(messageID)
parser.setMessage(message)
data = parser.encode()
print('SNPubrec')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNPubrec):
    if messageDecoded.getMessageID() == messageID:
        print('SNPubrec is Ok')
    else:
        print('SNPubrec Error occured')

print('_____________________________________')
#SNPubrel
messageID = 5
message = SNPubrel(messageID)
parser.setMessage(message)
data = parser.encode()
print('SNPubrel')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNPubrel):
    if messageDecoded.getMessageID() == messageID:
        print('SNPubrel is Ok')
    else:
        print('SNPubrel Error occured')

print('_____________________________________')
#SNSubscribe
messageID = 12
qos = QoS(1)
value = 'topicName'
topic = FullTopic(value, qos)
dup = False
message = SNSubscribe(messageID,topic,dup)
parser.setMessage(message)
data = parser.encode()
print('SNSubscribe')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNSubscribe):
    topic = messageDecoded.getTopic()
    if isinstance(topic, FullTopic):
        if topic.value == value and topic.getQoS() == qos.getValue() and messageDecoded.isDup() == dup:
            print('SNSubscribe is Ok')
        else:
            print('SNSubscribe Error occured error fields')
    else:
        print('SNSubscribe Error occured. it is not FullTopic')
        
print('_____________________________________')
#SNSuback
#topicID, code, qos, messageID
topicID = 12
code = ReturnCode.CONGESTION.value[0]
messageID = 13
qos = QoS(1)
message = SNSuback(topicID,code,qos,messageID)
parser.setMessage(message)
data = parser.encode()
print('SNSuback')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNSuback):
        if messageDecoded.getMessageID() == messageID and messageDecoded.getTopicID() == topicID and messageDecoded.getCode() == code and messageDecoded.getQoS() == qos.getValue():
            print('SNSuback is Ok')
        else:
            print('SNSuback Error occured error fields')
            print('messageID '+ str(messageDecoded.getMessageID()))
            print('topicID ' + str(messageDecoded.getTopicID()))
            print('code ' + str(messageDecoded.getCode()))
            print('qos ' + str(messageDecoded.getQoS()))

print('_____________________________________')
#SNUnsubscribe
messageID = 12
qos = QoS(0)
value = 'topicName'
topic = FullTopic(value, qos)
message = SNUnsubscribe(messageID,topic)
parser.setMessage(message)
data = parser.encode()
print('SNSubscribe')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNUnsubscribe):
    topic = messageDecoded.getTopic()
    if isinstance(topic, FullTopic):
        if topic.getValue() == value and topic.getQoS() == qos.getValue() and messageDecoded.getMessageID() == messageID:
            print('SNUnsubscribe is Ok')
        else:
            print('SNUnsubscribe Error occured error fields')
            print('value ' + str(topic.getValue()))
            print('qos ' + str( topic.getQoS()))
            print('messageID ' + str(messageDecoded.getMessageID()))
    else:
        print('SNUnsubscribe Error occured. it is not FullTopic')

print('_____________________________________')
#SNUnsuback
messageID = 5
message = SNUnsuback(messageID)
parser.setMessage(message)
data = parser.encode()
print('SNUnsuback')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNUnsuback):
    if messageDecoded.getMessageID() == messageID:
        print('SNUnsuback is Ok')
    else:
        print('SNUnsuback Error occured')

print('_____________________________________')
#SNPingreq
clientID = 'testclientID'
message = SNPingreq(clientID)
parser.setMessage(message)
data = parser.encode()
print('SNPingreq')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNPingreq):
    if messageDecoded.getClientID() == clientID:
        print('SNPingreq is Ok')
    else:
        print('SNPingreq Error occured')

print('_____________________________________')
#SNDisonnect
duration = 55
message = SNDisonnect(duration)
parser.setMessage(message)
data = parser.encode()
print('SNDisonnect')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, SNDisonnect):
    if messageDecoded.getDuration() == duration:
        print('SNDisonnect is Ok')
    else:
        print('SNDisonnect Error occured')

print('_____________________________________')
#WillTopicUpd
retain = True
qos = QoS(0)
value = 'topicName'
topic = FullTopic(value, qos)
message = WillTopicUpd(retain,topic)
parser.setMessage(message)
data = parser.encode()
print('WillTopicUpd')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, WillTopicUpd):
    topic = messageDecoded.getTopic()
    if isinstance(topic, FullTopic):
        if topic.getValue() == value and topic.getQoS() == qos.getValue() and messageDecoded.isRetain() == retain:
            print('WillTopicUpd is Ok')
        else:
            print('WillTopicUpd Error occured error fields')
            print('value ' + str(topic.getValue()))
            print('qos ' + str( topic.getQoS()))
            print('retain ' + str(messageDecoded.isRetain()))
    else:
        print('WillTopicUpd Error occured. it is not FullTopic')

print('_____________________________________')
#WillTopicResp
code = ReturnCode.INVALID_TOPIC_ID.value[0]
message = WillTopicResp(code)
parser.setMessage(message)
data = parser.encode()
print('SNPuback')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, WillTopicResp):
    if messageDecoded.getCode() == code:
        print('WillTopicResp is Ok')
    else:
        print('WillTopicResp Error occured')

print('_____________________________________')
#WillMsgUpd
content = 'testContentString'
message = WillMsgUpd(content)
parser.setMessage(message)
data = parser.encode()
print('WillMsgUpd')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, WillMsgUpd):
    if messageDecoded.getContent() == content:
        print('WillMsgUpd is Ok')
    else:
        print('WillMsgUpd Error occured')

print('_____________________________________')
#WillMsgResp
code = ReturnCode.INVALID_TOPIC_ID.value[0]
message = WillMsgResp(code)
parser.setMessage(message)
data = parser.encode()
print('WillMsgResp')
print('data: ' + str(data))
messageDecoded = parser.decode(data)
if isinstance(messageDecoded, WillTopicResp):
    if messageDecoded.getCode() == code:
        print('WillMsgResp is Ok')
    else:
        print('WillMsgResp Error occured')