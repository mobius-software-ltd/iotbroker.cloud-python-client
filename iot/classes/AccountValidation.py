class AccountValidation:

    def valid(account):
        if account.protocol == 1:
            if (account.username and account.password and account.clientID and account.serverHost and int(account.port)>0 and account.keepAlive and int(account.keepAlive)>0 and int(account.keepAlive)<65535):
                return True
            else:
                return False

        if account.protocol == 2:
            if (account.username and account.password and account.clientID and account.serverHost and int(account.port)>0 and account.keepAlive and int(account.keepAlive)>0 and int(account.keepAlive)<64800):
                return True
            else:
                return False

        if account.protocol == 3:
            if (account.clientID and account.serverHost and int(account.port)>0 and account.keepAlive and int(account.keepAlive)>0 and int(account.keepAlive)<64800):
                return True
            else:
                return False

        if account.protocol == 4:
            if (account.username and account.password and account.clientID and account.serverHost and int(account.port)>0 and account.keepAlive and int(account.keepAlive)>0 and int(account.keepAlive)<65535):
                return True
            else:
                return False

protocols = ['mqtt', 'mqttsn', 'coap', 'websocket']