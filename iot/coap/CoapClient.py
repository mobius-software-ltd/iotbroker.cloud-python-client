"""
 # Mobius Software LTD
 # Copyright 2015-2018, Mobius Software LTD
 #
 # This is free software; you can redistribute it and/or modify it
 # under the terms of the GNU Lesser General Public License as
 # published by the Free Software Foundation; either version 2.1 of
 # the License, or (at your option) any later version.
 #
 # This software is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this software; if not, write to the Free
 # Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 # 02110-1301 USA, or see the FSF site: http://www.fsf.org.
"""
import asyncio

from OpenSSL.crypto import X509

from iot.classes.IoTClient import *
from iot.coap.options.OptionParser import *
from iot.coap.tlv.CoapTopic import *
from iot.network.UDPClient import *
from iot.network.pyDTLSClient import *
from iot.timers.TimersMap import *

basicConfig(level=DEBUG)  # set now for dtls import code
from dtls import do_patch, wrapper

do_patch()
from threading import Thread
import socket
from socket import socket
from twisted.internet import reactor

import OpenSSL.crypto


class CoapClient(IoTClient):
    def __init__(self, account, client):
        self.account = account
        self.clientGUI = client
        self.parser = CoapParser()
        self.parserOption = OptionParser()
        self.resendperiod = 3000
        self.connectionState = None
        self.data = None
        self.udpClient = None
        self.timers = TimersMap(self)
        self.Version = 1
        self.forPublish = {}
        self.forSubscribe = {}
        self.forUnsubscribe = {}
        self.pingNum = 0
        self.udpThread = None
        self.ping_timer_started = False
        self.disconnected = False

    def goConnect(self):
        self.setState(ConnectionState.CONNECTING)

        duration = self.account.keepAlive

        if self.timers is not None:
            self.timers.stopAllTimers()

        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options = []
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.PUT, 0, None, options, None)

        if self.account.isSecure:

            self.loop = asyncio.new_event_loop()

            addr = (self.account.serverHost, self.account.port)
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.settimeout(5)
            sock.setblocking(1)
            if self.account.certificate and len(self.account.certificate) > 0:
                fp = self.get_certificate_file(self.account.certificate, self.account.certPasw)
                self.sock_wrapped = wrapper.wrap_client(sock, keyfile=fp.name, certfile=fp.name, ca_certs=fp.name)
            else:
                self.sock_wrapped = wrapper.wrap_client(sock)

            self.sock_wrapped.connect(addr)

            datagram_endpoint = self.loop.create_datagram_endpoint(lambda: pyDTLSClient(self.account.serverHost, self.account.port, self.account.certificate, self, self.loop), sock=self.sock_wrapped)

            self.transport, protocol = self.loop.run_until_complete(datagram_endpoint)
            self.udpClient = protocol
            self.setState(ConnectionState.CONNECTION_ESTABLISHED)

            self.udpThread = Thread(target=self.init_loop)
            self.udpThread.daemon = True
            self.udpThread.start()
        else:
            self.udpClient = UDPClient(self.account.serverHost, self.account.port, self)
            self.udp_listener = reactor.listenUDP(0, self.udpClient)

        self.timers.goConnectTimer(message)

    def init_loop(self):
        self.loop.run_forever()
        self.transport.close()
        self.loop.close()
        self.udpClient.connection_lost(None)
        try:
            self.sock_wrapped._sock.close()
        except:
            pass

    def stop_udp_listener(self):
        if hasattr(self, "loop") and self.loop is not None:
            self.loop.stop()
            try:
                self.sock_wrapped._sock.close()
            except Exception as ex:
                pass
        elif hasattr(self, "udp_listener"):
            self.udp_listener.stopListening()

    def get_certificate_file(self, cert_body, cert_pwd):

        fp = tempfile.NamedTemporaryFile()
        fp.write(bytes(cert_body, 'utf-8'))
        fp.seek(0)

        if cert_pwd is not None and len(cert_pwd) > 0:
            try:
                cert: X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, fp.read())
                fp.seek(0)
                key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, fp.read(), cert_pwd.encode("utf-8"))
                fp1 = tempfile.NamedTemporaryFile()
                fp1.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))
                fp1.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
                fp1.seek(0)
            except Exception as err:
                fp.close()
                raise err

            return fp1
        else:
            return fp

    def send(self, message):
        if self.connectionState == ConnectionState.CONNECTION_ESTABLISHED:
            message = self.parser.encode(message)
            self.udpClient.sendMessage(message)
        else:
            return False

    def refresh_ping_timer(self):
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options = []
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.PUT, 0, None, options, None)
        reactor.callFromThread(self.timers.goPingTimer, message, self.account.keepAlive)

    def dataReceived(self, data):
        message = self.parser.decode(data)

        type = message.getType()
        code = message.getCode()
        if code == CoapCode.POST or code == CoapCode.PUT:
            if type != CoapType.ACKNOWLEDGEMENT:
                topic = None
                qosValue = None
                for option in message.getOptionsDecode():
                    if isinstance(option, CoapOption):
                        if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                            topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                            break
                for option in message.getOptionsDecode():
                    if isinstance(option, CoapOption):
                        if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                            qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                            break
                if len(topic) > 0:
                    content = message.getPayload()
                    qos = QoS(qosValue)
                    topicResult = CoapTopic(topic, qos)
                    reactor.callFromThread(self.clientGUI.publishReceived, topicResult, qos, content, False, False)
                else:
                    textFormat = "text/plain"
                    options = []
                    option = self.parserOption.encode(CoapOptionType.CONTENT_FORMAT, textFormat)
                    options.append(option)
                    option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
                    options.append(option)
                    ack = CoapMessage(self.Version, CoapType.ACKNOWLEDGEMENT, CoapCode.BAD_OPTION, message.getPacketID(), message.getToken(), options, None)
                    self.send(ack)
            else:
                if not self.ping_timer_started:
                    self.timers.stopConnectTimer()
                    self.ping_timer_started = True
                    self.refresh_ping_timer()

        process_messageType_method(self, message.getType().value, message)

    def setState(self, ConnectionState):
        self.connectionState = ConnectionState

    def getConnectionState(self):
        return self.connectionState

    def publish(self, topicName, qosValue, content, retain, dup):
        options = []
        option = self.parserOption.encode(CoapOptionType.URI_PATH, topicName)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.ACCEPT, qosValue)
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.PUT, 0, '0', options, content)
        packetID = self.timers.goMessageTimer(message)
        message.setPacketID(packetID)
        self.forPublish[packetID] = message

    def subscribeTo(self, topicName, qosValue):
        options = []
        option = self.parserOption.encode(CoapOptionType.OBSERVE, 0)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.URI_PATH, topicName)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.ACCEPT, qosValue)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.GET, 0, '0', options, None)
        packetID = self.timers.goMessageTimer(message)
        message.setPacketID(packetID)
        self.forSubscribe[packetID] = message

    def unsubscribeFrom(self, topicName):
        options = []
        option = self.parserOption.encode(CoapOptionType.OBSERVE, 1)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.URI_PATH, topicName)
        options.append(option)
        option = self.parserOption.encode(CoapOptionType.ACCEPT, 0)
        options.append(option)
        message = CoapMessage(self.Version, CoapType.CONFIRMABLE, CoapCode.GET, 0, '0', options, None)
        packetID = self.timers.goMessageTimer(message)
        message.setPacketID(packetID)
        self.forUnsubscribe[packetID] = message

    def pingreq(self):
        reactor.callFromThread(self.clientGUI.connackReceived, None)

    def disconnectWith(self, duration):
        self.disconnected = True
        self.timers.stopAllTimers()
        self.stop_udp_listener()

    def timeoutMethod(self):
        self.error_occured("Timeout was reached. Try to reconnect")

    def process_connection_closed(self):
        self.timers.stopAllTimers()
        if not self.disconnected:
            self.error_occurred("Connection closed by server")

    def error_occurred(self, message):
        self.timers.stopAllTimers()
        self.stop_udp_listener()
        reactor.callFromThread(self.clientGUI.show_error_message, "Warning", message)
        reactor.callFromThread(self.clientGUI.errorReceived)

    def connectTimeoutMethod(self):
        self.timers.stopAllTimers()
        self.stop_udp_listener()
        reactor.callFromThread(self.clientGUI.show_error_message, "Connect Error", "Connection Timeout")
        reactor.callFromThread(self.clientGUI.errorReceived)

    def ConnectionLost(self):
        self.setState(ConnectionState.CONNECTION_LOST)
        self.stop_udp_listener()

    def connected(self):
        self.setState(ConnectionState.CHANNEL_ESTABLISHED)

    def connectFailed(self):
        self.setState(ConnectionState.CHANNEL_FAILED)
        self.stop_udp_listener()


# __________________________________________________________________________________________

def CONFIRMABLE(self, message):
    if isinstance(message, CoapMessage):
        options = []
        option = self.parserOption.encode(CoapOptionType.NODE_ID, self.account.clientID)
        options.append(option)
        ack = CoapMessage(self.Version, CoapType.ACKNOWLEDGEMENT, message.getCode(), message.getPacketID(), message.getToken(), options, None)
        self.send(ack)


def NONCONFIRMABLE(self, message):
    if isinstance(message, CoapMessage):
        self.timers.removeTimer(int(message.getToken()))


def ACKNOWLEDGEMENT(self, message):
    if isinstance(message, CoapMessage):
        ack = None
        topic = None
        qosValue = None
        if message.getToken() is not None:
            ack = self.timers.removeTimer(int(message.getToken()))
            if message.getCode() == CoapCode.CONTENT:
                for option in message.getOptionsDecode():
                    if isinstance(option, CoapOption):
                        if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                            topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                            break
                for option in message.getOptionsDecode():
                    if isinstance(option, CoapOption):
                        if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                            qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                            break
                if len(topic) > 0:
                    content = message.getPayload()
                    qos = QoS(qosValue)
                    topicResult = CoapTopic(topic, qos)
                    reactor.callFromThread(self.clientGUI.publishReceived, topicResult, qos, content, False, False)
        if ack is not None:
            if isinstance(ack, CoapMessage):
                if ack.getCode() == CoapCode.GET:
                    observeValue = None
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.OBSERVE:
                                observeValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                                topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                                qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    if observeValue == 0:
                        qos = QoS(qosValue)
                        reactor.callFromThread(self.clientGUI.subackReceived, topic, qos, 0)
                    elif observeValue == 1:
                        list = []
                        list.append(topic)
                        reactor.callFromThread(self.clientGUI.unsubackReceived, list)
                elif ack.getCode() == CoapCode.PUT:
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.URI_PATH:
                                topic = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    for option in ack.getOptionsDecode():
                        if isinstance(option, CoapOption):
                            if CoapOptionType(option.getType()) == CoapOptionType.ACCEPT:
                                qosValue = self.parserOption.decode(CoapOptionType(option.getType()), option)
                                break
                    content = ack.getPayload()
                    qos = QoS(qosValue)
                    topicResult = CoapTopic(topic, qos)
                    reactor.callFromThread(self.clientGUI.pubackReceived, topicResult, qos, content, False, False, 0)
        else:
            if self.pingNum == 0:
                self.pingNum += 1
                reactor.callFromThread(self.clientGUI.pingrespReceived, True)


def RESET(self, message):
    if isinstance(message, CoapMessage):
        self.timers.removeTimer(int(message.getToken()))


switcherProcess = {
    0: CONFIRMABLE,
    1: NONCONFIRMABLE,
    2: ACKNOWLEDGEMENT,
    3: RESET
}


def process_messageType_method(self, argument, message):
    return switcherProcess[argument].__call__(self, message)
