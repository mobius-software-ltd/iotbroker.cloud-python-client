class MQTT:

    def __init__(self):
        self.name = "mqtt"
        self.num = 1
        self.qos_list = ["0", "1", "2"]
        self.max_message_length = TCP_MAX_MESSAGE_LENGTH

    def is_tcp(self):
        return True

    def is_udp(self):
        return False


class MQTT_SN:

    def __init__(self):
        self.name = "mqttsn"
        self.num = 2
        self.qos_list = ["0", "1", "2"]
        self.max_message_length = UDP_MAX_MESSAGE_LENGTH

    def is_tcp(self):
        return False

    def is_udp(self):
        return True


class COAP:

    def __init__(self):
        self.name = "coap"
        self.num = 3
        self.qos_list = ["0", "1"]
        self.max_message_length = UDP_MAX_MESSAGE_LENGTH

    def is_tcp(self):
        return False

    def is_udp(self):
        return True


class WEBSOCKET:

    def __init__(self):
        self.name = "websocket"
        self.num = 4
        self.qos_list = ["0", "1", "2"]
        self.max_message_length = TCP_MAX_MESSAGE_LENGTH

    def is_tcp(self):
        return True

    def is_udp(self):
        return False


class AMQP:

    def __init__(self):
        self.name = "amqp"
        self.num = 5
        self.qos_list = ["1"]
        self.max_message_length = TCP_MAX_MESSAGE_LENGTH

    def is_tcp(self):
        return True

    def is_udp(self):
        return False


TCP_MAX_MESSAGE_LENGTH = 1500
UDP_MAX_MESSAGE_LENGTH = 1400
__protocols = [MQTT(), MQTT_SN(), COAP(), WEBSOCKET(), AMQP()]


def protocol_names():
    return [p.name for p in __protocols]


def get_protocol_name(num):
    for protocol in __protocols:
        if protocol.num == num:
            return protocol.name
    raise ValueError("invalid protocol value: " + num)


def get_protocol_num(name):
    for protocol in __protocols:
        if protocol.name == name:
            return protocol.num
    raise ValueError("invalid protocol value: " + name)


def is_tcp(protocol_val):
    for protocol in __protocols:
        if protocol.name == protocol_val or protocol.num == protocol_val:
            return protocol.is_tcp()
    raise ValueError("invalid protocol value: " + protocol_val)


def is_udp(protocol_val):
    for protocol in __protocols:
        if protocol.name == protocol_val or protocol.num == protocol_val:
            return protocol.is_udp()
    raise ValueError("invalid protocol value: " + protocol_val)


def qos_list(protocol_val):
    for protocol in __protocols:
        if protocol.name == protocol_val or protocol.num == protocol_val:
            return protocol.qos_list
    raise ValueError("invalid protocol value: " + protocol_val)


def is_message_length_valid(protocol_val, msg_length):
    return msg_length <= get_max_message_length(protocol_val)


def get_max_message_length(protocol_val):
    for protocol in __protocols:
        if protocol.name == protocol_val or protocol.num == protocol_val:
            return protocol.max_message_length
    raise ValueError("invalid protocol value: " + protocol_val)