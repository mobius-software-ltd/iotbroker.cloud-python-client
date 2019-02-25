import tkinter
from twisted.internet import tksupport

root = tkinter.Tk()
tksupport.install(root)

from twisted.internet import reactor
reactor.callLater(3, reactor.stop)
reactor.run()