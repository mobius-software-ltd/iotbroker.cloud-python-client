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
import protocol as client_protocol


def validate_message_length(protocol_value, msg):
    print("msg length=" + str(len(msg)))
    return client_protocol.is_message_length_valid(protocol_value, len(msg))


class AccountValidation:

    def valid(account):
        try:
            if account.protocol == 1:
                if validate_message_length(account.protocol, account.will) and account.username and account.password and account.clientID and account.serverHost and int(account.port) > 0 and account.keepAlive and int(account.keepAlive) > 0 and int(account.keepAlive) < 65535:
                    return True
                else:
                    return False

            if account.protocol == 2:
                if validate_message_length(account.protocol, account.will) and account.clientID and account.serverHost and int(account.port) > 0 and account.keepAlive and int(account.keepAlive) > 0 and int(account.keepAlive) < 65535:
                    return True
                else:
                    return False

            if account.protocol == 3:
                if validate_message_length(account.protocol, account.will) and account.clientID and account.serverHost and int(account.port) > 0 and account.keepAlive and int(account.keepAlive) > 0 and int(account.keepAlive) < 64800:
                    return True
                else:
                    return False

            if account.protocol == 4:
                if validate_message_length(account.protocol, account.will) and account.username and account.password and account.clientID and account.serverHost and int(account.port) > 0 and account.keepAlive and int(account.keepAlive) > 0 and int(account.keepAlive) < 65535:
                    return True
                else:
                    return False

            if account.protocol == 5:
                if validate_message_length(account.protocol, account.will) and account.username and account.password and account.clientID and account.serverHost and int(account.port) > 0 and account.keepAlive and int(account.keepAlive) > 0 and int(account.keepAlive) < 65535:
                    return True
                else:
                    return False
        except:
            return False
