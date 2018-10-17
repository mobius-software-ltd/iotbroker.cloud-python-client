import wx
import time
import sys

from database import AccountEntity, TopicEntity, MessageEntity, Base, datamanager
from venv.iot.classes.AccountValidation import  *

from twisted.python import log
from twisted.internet import wxreactor

from wx.lib.agw import ultimatelistctrl as ULC

wxreactor.install()

#import t.i.reactor only after installing wxreactor
from twisted.internet import reactor

from venv.iot.mqtt.MQTTclient import *
from venv.iot.mqttsn.MQTTSNclient import *
from venv.iot.coap.CoapClient import *
import platform

#GUI---------------------------------------------------------------------------------------------------------------------GUI
class LoadingForm(wx.Frame):
    def __init__(self, parent, ID, title, app):
        self.app = app
        wx.Frame.__init__(self, parent, ID, title,size=wx.Size(360,500))
        self.Centre()
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        self.timer = wx.Timer(self, 1)
        self.count = 0

        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        iconBox = wx.BoxSizer(wx.HORIZONTAL)
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        statusBox = wx.BoxSizer(wx.HORIZONTAL)

        iconBig = wx.Image("./resources/iotbroker_icon_big.png", wx.BITMAP_TYPE_ANY)
        self.imageIcon = wx.StaticBitmap(panel, wx.ID_ANY,wx.Bitmap(iconBig))
        loadText = wx.Image("./resources/ic_loading_text.png", wx.BITMAP_TYPE_ANY)
        self.imageText = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(loadText))

        self.gauge = wx.Gauge(panel, 100, size=(250, 25))

        iconBox.Add(self.imageIcon, 1, wx.ALIGN_CENTRE)
        textBox.Add(self.imageText, 1, wx.ALIGN_CENTRE)
        statusBox.Add(self.gauge, 1, wx.ALIGN_CENTRE)

        vbox.Add((0, 10), 0)
        vbox.Add(iconBox, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 10), 0)
        vbox.Add(textBox, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 20), 0)
        vbox.Add(statusBox, 1, wx.ALIGN_CENTRE)

        panel.SetSizer(vbox)

        self.Centre()
        self.timer.Start(10)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

    def OnTimer(self, event):

        self.count = self.count +1
        time.sleep(0.02)
        self.gauge.SetValue(self.count)
        self.gauge.Update()

        if self.count == 100:
            self.timer.Stop()
            #print("timer stopped")

            #if default account exists when connect else show accountsForm
            datamanage = datamanager()
            account = datamanage.get_default_account()

            if account is not None:
                #print('Default account: ' + str(account.clientID) + ' qos= ' + str(account.qos))
                print('connection to: ' + account.serverHost+":"+ str(account.port))

                if account.protocol == 1:
                    self.app.client = MQTTclient(account, self.app.gui)
                    self.app.client.goConnect()
                    self.Hide()

                if account.protocol == 2:
                    self.app.client = MQTTSNclient(account, self.app.gui)
                    self.app.client.goConnect()
                    self.Hide()

                if account.protocol == 3:
                   self.app.client = CoapClient(account, self.app.gui)
                   self.app.client.goConnect()
                   self.Hide()
                   #next = MainForm(None, -1, "Main", self.app.gui)
                   #next.Show()

                if account.protocol == 4:
                    print('Protocol= ' + str(protocols[account.protocol-1]))

            else:
                #print("show AccountsForm")
                self.Hide()
                next = AccountsForm(None, 1, "Accounts List", self.app)
                next.Show()

    def onClose(self, event):
        if self.app.client is not None:
            self.app.client.timers.stopAllTimers()
        reactor.stop()

class AccountsForm(wx.Frame):

    def __init__(self, parent, ID, title, app):
        self.app = app
        wx.Frame.__init__(self, parent, ID, title, size=wx.Size(360, 500))
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)
        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        topPanel = wx.Panel(self, size=wx.Size(360, 500))
        panelText = wx.Panel(self, -1, size=wx.Size(360, 50))
        panelList = wx.Panel(self, -1, size=wx.Size(360, 400))
        panelBtn = wx.Panel(self, -1, size=wx.Size(360, 50))

        self.text = wx.Button(panelText, label="Please select account", size=wx.Size(360, 50), style = wx.NO_BORDER)
        self.text.BitmapFocus = self.text.BitmapCurrent
        self.text.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.text.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.text.SetForegroundColour((255, 255, 255))

        self.list = ULC.UltimateListCtrl(panelList, wx.ID_ANY, agwStyle=ULC.ULC_NO_HEADER|wx.LC_REPORT|wx.LC_SINGLE_SEL|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnConnect, self.list)
        #self.list.SetFont(boldfont)

        self.list.InsertColumn(0, "Account")
        self.list.InsertColumn(1, "Button")

        self.list.SetColumnWidth(0, 300)
        self.list.SetColumnWidth(1, 59)

        self.list.SetSize(360, 400)

        datamanage = datamanager()
        accounts = datamanage.get_accounts_all()
        self.list.SetFont(font)

        if platform.system()=='Linux':
            bmp = wx.Bitmap("./resources/ic_delete_with_background.png", wx.BITMAP_TYPE_BMP)
        else:
            bmp = wx.Bitmap("./resources/ic_delete_with_background.bmp", wx.BITMAP_TYPE_BMP)

        i = 0
        if len(accounts) > 0:
            for item in accounts:
                self.btnDel = wx.BitmapButton(self.list, id=i, bitmap=bmp,
                                              size=(bmp.GetWidth() + 12, bmp.GetHeight() + 10), style = wx.NO_BORDER)
                self.Bind(wx.EVT_BUTTON, self.OnDelete, self.btnDel)
                self.list.InsertStringItem(i, str(item.username)+'\n'+ str(item.clientID) +'\n'+ str(item.serverHost + ":" + str(item.port)))
                self.list.SetItemWindow(i, 1, self.btnDel)
                i += 1

        self.btnCreate = wx.Button(panelBtn, label="CREATE", size=wx.Size(360, 50), style = wx.NO_BORDER)
        self.btnCreate.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.btnCreate.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnCreate.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.OnCreate, self.btnCreate)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panelText,wx.EXPAND|wx.ALL,border=0)
        sizer.Add(panelList,wx.EXPAND|wx.ALL,border=0)
        sizer.Add(panelBtn,wx.EXPAND|wx.ALL,border=0)

        topPanel.SetSizer(sizer)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        vbox.Fit(self)
        self.Layout()
        self.SetSizer(vbox)

    def OnConnect(self, event):
        list = event.GetEventObject()
        id = list.GetFocusedItem()
        # set ACCOUNT as default
        data = list.GetItem(id, 0).GetText()
        params = data.split('\n')
        clientID = str(params[1])
        datamanage = datamanager()
        datamanage.clear_default_account()
        account = datamanage.set_default_account_clientID(clientID)
        self.Hide()
        next = LoadingForm(None, -1, "Loading", self.app)
        next.Show()

    def OnDelete(self, event):
        btn = event.GetEventObject()
        id = btn.GetId()

        data = self.list.GetItem(id, 0).GetText()
        params = data.split('\n')
        clientID = str(params[1])

        accountID = id
        datamanage = datamanager()
        account = datamanage.delete_account(clientID)
        self.list.DeleteItem(id)

    def OnCreate(self, event):
        self.Hide()
        next = LoginForm(None, -1, "Login", self.app)
        next.Show()

    def onClose(self, event):
        if self.app.client is not None:
            self.app.client.timers.stopAllTimers()
        reactor.stop()

class LoginForm(wx.Frame):
    def __init__(self, parent, ID, title, app):
        self.app = app
        wx.Frame.__init__(self, parent, ID, title,size=wx.Size(360, 540))
        self.Centre()
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        topPanel = wx.Panel(self, size=wx.Size(360, 600))

        panel1 = wx.Panel(self, -1,size=wx.Size(360,210))
        panel1.SetBackgroundColour((255, 255, 255))

        panel2 = wx.Panel(self, -1,size=wx.Size(360,210))
        panel2.SetBackgroundColour((255, 255, 255))

        fontBold = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

        regInfo = wx.StaticText(topPanel, -1, "  registration info:")
        regInfo.SetFont(fontBold)

        imgSettings = wx.Image("./resources/settings.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlSettings = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.protocolLabel = wx.StaticText(panel1, -1, "Protocol:", )
        self.protocolLabel.SetFont(font)
        self.comboProtocol = wx.ComboBox(panel1, -1, 'mqtt', choices=protocols)

        imgSettings = wx.Image("./resources/username.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlName = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.nameLabel = wx.StaticText(panel1, -1, "Username:")
        self.nameLabel.SetFont(font)
        self.nameText = wx.TextCtrl(panel1, size=wx.Size(150, 30))

        imgSettings = wx.Image("./resources/password.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlPasw = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.paswLabel = wx.StaticText(panel1, -1, "Password:")
        self.paswLabel.SetFont(font)
        self.paswText = wx.TextCtrl(panel1, size=wx.Size(150, 30))

        imgSettings = wx.Image("./resources/clienid.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlclient = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.idLabel = wx.StaticText(panel1, -1, "Client ID:")
        self.idLabel.SetFont(font)
        self.idText = wx.TextCtrl(panel1, size=wx.Size(150, 30))

        imgSettings = wx.Image("./resources/host.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlhost = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.hostLabel = wx.StaticText(panel1, -1, "Server host:")
        self.hostLabel.SetFont(font)
        self.hostText = wx.TextCtrl(panel1, size=wx.Size(150, 30))

        self.imageCtrlport = wx.StaticBitmap(panel1, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.portLabel = wx.StaticText(panel1, -1, "Port:")
        self.portLabel.SetFont(font)
        self.portText = wx.TextCtrl(panel1, size=wx.Size(150, 30))

        imgSettings = wx.Image("./resources/cleansession.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlclean = wx.StaticBitmap(panel2, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.cleanLabel = wx.StaticText(panel2, -1, "Clean session:")
        self.cleanLabel.SetFont(font)
        self.cleanCheck = wx.CheckBox(panel2)

        imgSettings = wx.Image("./resources/keepalive.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlkeep = wx.StaticBitmap(panel2, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.keepLabel = wx.StaticText(panel2, -1, "Keepalive:")
        self.keepLabel.SetFont(font)
        self.keepText = wx.TextCtrl(panel2, size=wx.Size(150, 30))

        imgSettings = wx.Image("./resources/settings.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlwillT = wx.StaticBitmap(panel2, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.willTLabel = wx.StaticText(panel2, -1, "Will topic:")
        self.willTLabel.SetFont(font)
        self.willTText = wx.TextCtrl(panel2, size=wx.Size(150, 30))

        self.imageCtrlwill = wx.StaticBitmap(panel2, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.willLabel = wx.StaticText(panel2, -1, "Will:")
        self.willLabel.SetFont(font)
        self.willText = wx.TextCtrl(panel2, size=wx.Size(150, 30))

        self.imageCtrlretain = wx.StaticBitmap(panel2, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.retainLabel = wx.StaticText(panel2, -1, "Retain:")
        self.retainLabel.SetFont(font)
        self.retainCheck = wx.CheckBox(panel2)

        self.imageCtrlqos = wx.StaticBitmap(panel2, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.qosLabel = wx.StaticText(panel2, -1, "QoS:")
        self.qosLabel.SetFont(font)
        self.comboQos = wx.ComboBox(panel2, -1, '0', choices=qos)

        settings = wx.StaticText(topPanel, -1, "  settings:")
        settings.SetFont(fontBold)

        panel1_vertical = wx.BoxSizer(wx.VERTICAL)
        protocol_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        username_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        pasw_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        clientId_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        host_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        port_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        protocol_horizontal.AddSpacer(10)
        protocol_horizontal.Add(self.imageCtrlSettings, wx.LEFT, 20)
        protocol_horizontal.AddSpacer(10)
        protocol_horizontal.Add(self.protocolLabel)
        protocol_horizontal.AddSpacer(120)
        protocol_horizontal.Add(self.comboProtocol, 1, wx.RIGHT, 20)

        username_horizontal.AddSpacer(10)
        username_horizontal.Add(self.imageCtrlName, wx.LEFT, 20)
        username_horizontal.AddSpacer(10)
        username_horizontal.Add(self.nameLabel)
        username_horizontal.AddSpacer(64)
        username_horizontal.Add(self.nameText, 1, wx.RIGHT, 20)

        pasw_horizontal.AddSpacer(10)
        pasw_horizontal.Add(self.imageCtrlPasw, wx.LEFT, 20)
        pasw_horizontal.AddSpacer(10)
        pasw_horizontal.Add(self.paswLabel)
        pasw_horizontal.AddSpacer(73)
        pasw_horizontal.Add(self.paswText, 1, wx.RIGHT, 20)

        clientId_horizontal.AddSpacer(10)
        clientId_horizontal.Add(self.imageCtrlclient, wx.LEFT, 20)
        clientId_horizontal.AddSpacer(10)
        clientId_horizontal.Add(self.idLabel)
        clientId_horizontal.AddSpacer(80)
        clientId_horizontal.Add(self.idText, 1, wx.RIGHT, 20)

        host_horizontal.AddSpacer(10)
        host_horizontal.Add(self.imageCtrlhost, wx.LEFT, 20)
        host_horizontal.AddSpacer(10)
        host_horizontal.Add(self.hostLabel)
        host_horizontal.AddSpacer(56)
        host_horizontal.Add(self.hostText, 1, wx.RIGHT, 20)

        port_horizontal.AddSpacer(10)
        port_horizontal.Add(self.imageCtrlport, wx.LEFT, 20)
        port_horizontal.AddSpacer(10)
        port_horizontal.Add(self.portLabel)
        port_horizontal.AddSpacer(115)
        port_horizontal.Add(self.portText, 1, wx.RIGHT, 20)

        panel1_vertical.AddSpacer(5)
        panel1_vertical.Add(protocol_horizontal)
        panel1_vertical.AddSpacer(5)
        panel1_vertical.Add(username_horizontal)
        panel1_vertical.AddSpacer(5)
        panel1_vertical.Add(pasw_horizontal)
        panel1_vertical.AddSpacer(5)
        panel1_vertical.Add(clientId_horizontal)
        panel1_vertical.AddSpacer(5)
        panel1_vertical.Add(host_horizontal)
        panel1_vertical.AddSpacer(5)
        panel1_vertical.Add(port_horizontal)

        panel1.SetSizer(panel1_vertical)

        panel2_vertical = wx.BoxSizer(wx.VERTICAL)
        clean_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        alive_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        willt_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        will_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        retain_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        qos_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        clean_horizontal.AddSpacer(10)
        clean_horizontal.Add(self.imageCtrlclean)
        clean_horizontal.AddSpacer(10)
        clean_horizontal.Add(self.cleanLabel)
        clean_horizontal.AddSpacer(165)
        clean_horizontal.Add(self.cleanCheck, 1, wx.RIGHT, 20)

        alive_horizontal.AddSpacer(10)
        alive_horizontal.Add(self.imageCtrlkeep)
        alive_horizontal.AddSpacer(10)
        alive_horizontal.Add(self.keepLabel)
        alive_horizontal.AddSpacer(70)
        alive_horizontal.Add(self.keepText, 1, wx.RIGHT, 20)

        willt_horizontal.AddSpacer(10)
        willt_horizontal.Add(self.imageCtrlwill)
        willt_horizontal.AddSpacer(10)
        willt_horizontal.Add(self.willLabel)
        willt_horizontal.AddSpacer(120)
        willt_horizontal.Add(self.willText, 1, wx.RIGHT, 20)

        will_horizontal.AddSpacer(10)
        will_horizontal.Add(self.imageCtrlwillT)
        will_horizontal.AddSpacer(10)
        will_horizontal.Add(self.willTLabel)
        will_horizontal.AddSpacer(75)
        will_horizontal.Add(self.willTText, 1, wx.RIGHT, 20)

        retain_horizontal.AddSpacer(10)
        retain_horizontal.Add(self.imageCtrlretain)
        retain_horizontal.AddSpacer(10)
        retain_horizontal.Add(self.retainLabel)
        retain_horizontal.AddSpacer(225)
        retain_horizontal.Add(self.retainCheck, 1, wx.RIGHT, 20)

        qos_horizontal.AddSpacer(10)
        qos_horizontal.Add(self.imageCtrlqos)
        qos_horizontal.AddSpacer(10)
        qos_horizontal.Add(self.qosLabel)
        qos_horizontal.AddSpacer(205)
        qos_horizontal.Add(self.comboQos, 1, wx.RIGHT, 20)

        panel2_vertical.AddSpacer(5)
        panel2_vertical.Add(clean_horizontal)
        panel2_vertical.AddSpacer(5)
        panel2_vertical.Add(alive_horizontal)
        panel2_vertical.AddSpacer(5)
        panel2_vertical.Add(willt_horizontal)
        panel2_vertical.AddSpacer(5)
        panel2_vertical.Add(will_horizontal)
        panel2_vertical.AddSpacer(5)
        panel2_vertical.Add(retain_horizontal)
        panel2_vertical.AddSpacer(5)
        panel2_vertical.Add(qos_horizontal)

        panel2.SetSizer(panel2_vertical)

        # BUTTON
        self.btn = wx.Button(topPanel, label="Log In", size=wx.Size(360, 50), style = wx.NO_BORDER)
        self.btn.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.btn.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btn.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(regInfo)
        sizer.AddSpacer(5)
        sizer.Add(panel1,0,wx.EXPAND|wx.ALL,border=0)
        sizer.AddSpacer(5)
        sizer.Add(settings)
        sizer.AddSpacer(5)
        sizer.Add(panel2,0,wx.EXPAND|wx.ALL,border=0)
        sizer.Add(self.btn)

        topPanel.SetSizer(sizer)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        self.SetSizer(vbox)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

    def OnOk(self, event):
        # create ACCOUNT and SAVE as default
        protocol = switch_protocol[self.comboProtocol.GetValue()]
        name = self.nameText.GetValue()
        password = self.paswText.GetValue()
        clientID = self.idText.GetValue()
        serverHost = self.hostText.GetValue()
        serverPort = self.portText.GetValue()
        cleanSession = self.cleanCheck.GetValue()
        keepAlive = self.keepText.GetValue()
        will = self.willText.GetValue()
        willT = self.willTText.GetValue()
        qos = self.comboQos.GetValue()

        account = AccountEntity(protocol=protocol, username=name, password=password, clientID=clientID,
                                serverHost=serverHost,
                                port=serverPort, cleanSession=cleanSession, keepAlive=keepAlive, will=will, willTopic=willT,
                                isRetain=True,
                                qos=qos, isDefault=False)


        if AccountValidation.valid(account):
            datamanage = datamanager()
            datamanage.add_entity(account)
            account = datamanage.get_account_clientID(clientID)
            datamanage.set_default_account_clientID(account.id)

            self.Hide()
            next = LoadingForm(None, -1, "Loading", self.app)
            next.Show()
        else:
            wx.MessageBox('Please, fill in all required fileds: Username, Password, ClientID, Host, Port, Keepalive', 'Warning',
                          wx.OK | wx.ICON_WARNING)

    def onClose(self, event):
        if self.app.client is not None:
            self.app.client.timers.stopAllTimers()
        reactor.stop()

def getNextImageID(count):
    print('here')
    imID = 0
    while True:
        yield imID

        imID += 1
    # end while
# end def

class ToolbookImpl(wx.Toolbook):

    def __init__(self, parent, app):
        wx.Toolbook.__init__(self, parent, wx.ID_ANY, style=wx.BG_STYLE_CUSTOM | wx.BK_BOTTOM | wx.NO_BORDER)
        # Make an image list using the LBXX images
        self.parent = parent
        self.app = app

        self.il = wx.ImageList(75, 41)
        tlist_img = wx.Bitmap("./resources/ic_topics_list_blue_75.png")
        send_img = wx.Bitmap("./resources/is_message_list_blue-1_75.png")
        mlist_img = wx.Bitmap("./resources/is_message_list_blue-03_75.png")
        logout_img = wx.Bitmap("./resources/logout75.png")

        tlist_img_blue = wx.Bitmap("./resources/ic_topics_list_blue-1_75.png")
        send_img_blue = wx.Bitmap("./resources/is_message_list_blue-2_75.png")
        mlist_img_blue = wx.Bitmap("./resources/is_message_list_blue-03-1_75.png")

        self.il.Add(tlist_img)
        self.il.Add(send_img)
        self.il.Add(mlist_img)
        self.il.Add(logout_img)

        self.il.Add(tlist_img_blue)
        self.il.Add(send_img_blue)
        self.il.Add(mlist_img_blue)

        self.AssignImageList(self.il)

        self.notebookPageList = [(TopicsPanel(self, app),  'Topics list'),
                            (SendPanel(self, app),    'Send message'),
                            (MessagesPanel(self, app),'Messages list'),
                            (LogoutPanel(self, app),  'Logout')]

        i = 0
        for page, label in self.notebookPageList:
            self.AddPage(page, label, imageId=i)
            i += 1
            if i == 4:
                break

        toolbar = self.GetToolBar()
        if platform.system() == 'Linux':
            toolbar.SetFont(wx.Font(7, wx.FONTBTN_DEFAULT_STYLE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        else:
            toolbar.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))

        toolbar.SetWindowStyle(style=wx.TB_FLAT)

        #self.ChangeSelection(1)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanging(self, event):
        new = event.GetSelection()
        print('OnPageChanging ' + str(new))

        if new == 0:
            self.SetPageImage(0,4)
        if new == 1:
            self.SetPageImage(1,5)
        if new == 2:
            self.SetPageImage(2,6)

        self.Refresh()

        if new == 3:
            self.parent.Hide()
            next = AccountsForm(None, 1, "Accounts List", self.parent.app)
            next.Show()
            #______________________________________________________________________SEND___DISCONNECT
            if self.parent.app.client is not None:
                self.parent.app.client.disconnectWith(0)
        event.Skip()

class MainForm(wx.Frame):
    def __init__(self, parent, ID, title, app):
        wx.Frame.__init__(self, parent, ID, title, size=wx.Size(360, 560))

        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.app = app
        self.Bind(wx.EVT_CLOSE, self.onClose)
        nb = ToolbookImpl(self, app)

        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, )
        nb.SetFont(font)

        nb.BackgroundColour = (255, 255, 255)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()

    def onClose(self, event):
        if self.app.client is not None:
            self.app.client.timers.stopAllTimers()
        reactor.stop()

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

class LogoutPanel(wx.Panel):
    def __init__(self, parent, app):
        self.app = app
        wx.Panel.__init__(self, parent)
        pass

class MyStaticText(wx.StaticText):
    def __init__(self,parent,id,label,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=0):
        wx.StaticText.__init__(self,parent,id,label,pos,size,style)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnPaint(self,event):
        dc = wx.PaintDC(self)
        dc.DrawText(self.GetLabelText(), 0, 0)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

class TopicsPanel(wx.Panel):
    def __init__(self, parent, app):

        self.app = app
        wx.Panel.__init__(self, parent)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)

        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        topPanel = wx.Panel(self, size=wx.Size(359, 560))
        panelText1 = wx.Panel(self, -1, size=wx.Size(359, 20), style= wx.NO_BORDER)
        panelList = wx.Panel(self, -1, size=wx.Size(359, 320))
        panelText2 = wx.Panel(self, -1, size=wx.Size(359, 20))
        panelTopic = wx.Panel(self, -1, size=wx.Size(359, 80))
        panelTopic.SetBackgroundColour((255, 255, 255))
        panelBtn = wx.Panel(self, -1, size=wx.Size(359, 50))

        text1 = MyStaticText(panelText1, -1, ' topics list:',size=wx.Size(359, 20))
        text2 = MyStaticText(panelText2, -1, ' add new topic:', size=wx.Size(359, 20))

        #self.timer = wx.Timer(self, 1)
        #self.count = 0
        #self.gauge = wx.Gauge(panelText, 100, size=(359, 5))
        #self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.list = ULC.UltimateListCtrl(panelList, wx.ID_ANY, agwStyle=ULC.ULC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.list.SetFont(boldfont)

        self.list.InsertColumn(0, "Topic")
        self.list.InsertColumn(1, "Qos")
        self.list.InsertColumn(2, "Button")

        self.list.SetColumnWidth(0, 250)
        self.list.SetColumnWidth(1, 50)
        self.list.SetColumnWidth(2, 50)

        self.list.SetSize(350, 315)

        datamanage = datamanager()
        account = datamanage.get_default_account()
        self.list.SetFont(font)

        if platform.system() == 'Linux':
            bmp = wx.Bitmap("./resources/ic_delete_with_background.png", wx.BITMAP_TYPE_BMP)
        else:
            bmp = wx.Bitmap("./resources/ic_delete_with_background.bmp", wx.BITMAP_TYPE_BMP)

        i = 0
        topics = None
        if account is not None:
            topics = datamanage.get_topics_all_accountID(account.id)

        if topics is not None:
            if len(topics)>0:
                for item in topics:
                    self.btnDel = wx.BitmapButton(self.list, id=i, bitmap=bmp,
                                                  size=(bmp.GetWidth() + 12, bmp.GetHeight() + 10), style=wx.NO_BORDER)
                    self.Bind(wx.EVT_BUTTON, self.OnDelete, self.btnDel)
                    self.list.InsertStringItem(i, str(item.topicName))

                    if platform.system() == 'Linux':
                        qosBmp = wx.Bitmap("./resources/icon_qos_0_75.png", wx.BITMAP_TYPE_BMP)
                        if item.qos == 1:
                            qosBmp = wx.Bitmap("./resources/icon_qos_1_75.png", wx.BITMAP_TYPE_BMP)
                        if item.qos == 2:
                            qosBmp = wx.Bitmap("./resources/icon_qos_2_75.png", wx.BITMAP_TYPE_BMP)
                    else:
                        qosBmp = wx.Bitmap("./resources/icon_qos_0_75.bmp", wx.BITMAP_TYPE_BMP)
                        if item.qos == 1:
                            qosBmp = wx.Bitmap("./resources/icon_qos_1_75.bmp", wx.BITMAP_TYPE_BMP)
                        if item.qos == 2:
                            qosBmp = wx.Bitmap("./resources/icon_qos_2_75.bmp", wx.BITMAP_TYPE_BMP)

                    self.imageCtrlQos = wx.StaticBitmap(self.list, wx.ID_ANY, wx.Bitmap(qosBmp))
                    self.list.SetItemWindow(i, 1, self.imageCtrlQos)
                    self.list.SetItemWindow(i, 2, self.btnDel)
                    if (i % 2) == 0:
                        self.list.SetItemBackgroundColour(i, wx.Colour(255, 255, 255))
                    else:
                        self.list.SetItemBackgroundColour(i, wx.Colour(224, 224, 224))
                    i += 1

        self.btnCreate = wx.Button(panelBtn, label="Add", size=wx.Size(370, 50), style = wx.NO_BORDER)
        self.btnCreate.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.btnCreate.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnCreate.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.OnCreate, self.btnCreate)

        sizer = wx.BoxSizer(wx.VERTICAL)

        imgSettings = wx.Image("./resources/settings.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlTopic = wx.StaticBitmap(panelTopic, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.TopicLabel = wx.StaticText(panelTopic, -1, "Topic:")
        self.TopicLabel.SetFont(font)
        self.nameText = wx.TextCtrl(panelTopic, size=wx.Size(150, 30))
        self.imageCtrlqos = wx.StaticBitmap(panelTopic, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.qosLabel = wx.StaticText(panelTopic, -1, "QoS:")
        self.qosLabel.SetFont(font)
        self.comboQos = wx.ComboBox(panelTopic, -1, '0', choices=qos)

        topic_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        qos_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        topic_horizontal.AddSpacer(10)
        topic_horizontal.Add(self.imageCtrlTopic, wx.LEFT, 20)
        topic_horizontal.AddSpacer(10)
        topic_horizontal.Add(self.TopicLabel)
        topic_horizontal.AddSpacer(95)
        topic_horizontal.Add(self.nameText, 1, wx.RIGHT, 20)

        qos_horizontal.AddSpacer(10)
        qos_horizontal.Add(self.imageCtrlqos, wx.LEFT, 20)
        qos_horizontal.AddSpacer(10)
        qos_horizontal.Add(self.qosLabel)
        qos_horizontal.AddSpacer(200)
        qos_horizontal.Add(self.comboQos, 1, wx.RIGHT, 20)

        panelTopic_vertical = wx.BoxSizer(wx.VERTICAL)
        panelTopic_vertical.AddSpacer(10)
        panelTopic_vertical.Add(topic_horizontal)
        panelTopic_vertical.AddSpacer(5)
        panelTopic_vertical.Add(qos_horizontal)

        panelTopic.SetSizer(panelTopic_vertical)

        headerBox1 = wx.BoxSizer(wx.VERTICAL)
        headerBox1.Add(text1)
        #headerBox.Add(self.gauge, wx.ALIGN_LEFT)
        #headerBox.Add((0, 5), 0)
        panelText1.SetSizer(headerBox1)
        headerBox2 = wx.BoxSizer(wx.VERTICAL)
        headerBox2.Add(text2)
        #headerBox2.Add((0, 5), 0)
        panelText2.SetSizer(headerBox2)

        buttonBox = wx.BoxSizer(wx.VERTICAL)
        buttonBox.Add(self.btnCreate)
        panelBtn.SetSizer(buttonBox)

        sizer.Add(panelText1, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelList, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelText2, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelTopic, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelBtn, wx.EXPAND | wx.ALL, border=0)

        topPanel.SetSizer(sizer)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        vbox.Fit(self)
        self.Layout()
        self.SetSizer(vbox)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

    def OnCreate(self, event):
        name = self.nameText.GetValue()
        qos = self.comboQos.GetValue()

        if name is not None and name != '':
            #ADD to list
            self.nameText.SetValue('');
            self.comboQos.SetValue('0');

            i = self.list.GetItemCount()
            bmp = wx.Bitmap("./resources/ic_delete_with_background.png", wx.BITMAP_TYPE_BMP)
            self.btnDel = wx.BitmapButton(self.list, id=i, bitmap=bmp,
                                          size=(bmp.GetWidth() + 12, bmp.GetHeight() + 10), style=wx.NO_BORDER)

            self.Bind(wx.EVT_BUTTON, self.OnDelete, self.btnDel)
            self.list.InsertStringItem(i, str(name))
            if (i % 2) == 0:
                self.list.SetItemBackgroundColour(i, wx.Colour(255, 255, 255))
            else:
                self.list.SetItemBackgroundColour(i, wx.Colour(224, 224, 224))

            qosBmp = None
            if platform.system() == 'Linux':
                qosBmp = wx.Bitmap("./resources/icon_qos_0_75.png", wx.BITMAP_TYPE_BMP)
                if int(qos) == 1:
                    qosBmp = wx.Bitmap("./resources/icon_qos_1_75.png", wx.BITMAP_TYPE_BMP)
                if int(qos) == 2:
                    qosBmp = wx.Bitmap("./resources/icon_qos_2_75.png", wx.BITMAP_TYPE_BMP)
            else:
                qosBmp = wx.Bitmap("./resources/icon_qos_0_75.bmp", wx.BITMAP_TYPE_BMP)
                if int(qos) == 1:
                    qosBmp = wx.Bitmap("./resources/icon_qos_1_75.bmp", wx.BITMAP_TYPE_BMP)
                if int(qos) == 2:
                    qosBmp = wx.Bitmap("./resources/icon_qos_2_75.bmp", wx.BITMAP_TYPE_BMP)
            self.imageCtrlQos = wx.StaticBitmap(self.list, wx.ID_ANY, wx.Bitmap(qosBmp))
            self.list.SetItemWindow(i, 1, self.imageCtrlQos)
            self.list.SetItemWindow(i, 2, self.btnDel)
            # SEND SUBSCRIBE _________________________________________________________________________________SEND SUBSCRIBE
            self.app.client.subscribeTo(name, int(qos))
            #self.timer.Start(1)
        else:
            wx.MessageBox('Please, fill in all required fields: TopicName', 'Warning',
                          wx.OK | wx.ICON_WARNING)

    def OnDelete(self, event):
        btn = event.GetEventObject()
        id = btn.GetId()
        topicName = self.list.GetItem(id, 0).GetText()

        # SEND UNSUBSCRIBE _________________________________________________________________________________SEND UNSUBSCRIBE
        self.app.client.unsubscribeFrom(topicName)
        #self.timer.Start(1)

    def OnTimer(self, event):
        self.count = self.count+1
        time.sleep(0.03)
        self.gauge.SetValue(self.count)
        self.gauge.Update()

        if self.count == 100:
            self.timer.Stop()
            self.count = 0
            self.gauge.SetValue(self.count)
            self.gauge.Update()

            #print("Suback or Unsuback is not received. Please, check state of your connection to server")
            wx.MessageBox('Suback or Unsuback is not received. Please, check state of your connection to server', 'Warning',
                          wx.OK | wx.ICON_WARNING)

class MessagesPanel(wx.Panel):
    def __init__(self, parent, app):
        self.app = app
        wx.Panel.__init__(self, parent)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)
        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        topPanel = wx.Panel(self, size=wx.Size(361, 560))
        panelText = wx.Panel(self, -1, size=wx.Size(360, 20))
        panelList = wx.Panel(self, -1, size=wx.Size(360, 470))

        text = MyStaticText(panelText, -1, ' messages list:', size=wx.Size(360, 20))

        self.list = ULC.UltimateListCtrl(panelList, wx.ID_ANY,
                                         agwStyle=ULC.ULC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        self.list.SetFont(boldfont)
        self.list.InsertColumn(0, "Topic")
        self.list.InsertColumn(1, "Qos")

        self.list.SetColumnWidth(0, 280)
        self.list.SetColumnWidth(1, 59)

        self.list.SetSize(350, 460)

        datamanage = datamanager()
        account = datamanage.get_default_account()
        self.list.SetFont(font)

        messages = None
        if account is not None:
            messages = datamanage.get_messages_all_accountID(account.id)

        i=0
        if messages is not None:
            if len(messages) > 0:
                for item in messages:
                    self.list.InsertStringItem(i, str(item.topicName) + '\n' + str(item.content))

                    if platform.system() == 'Linux':
                        if item.incoming:
                            if item.qos == 0:
                                bmp = wx.Bitmap("./resources/icon_in_qos_0_75.png", wx.BITMAP_TYPE_BMP)
                            if item.qos == 1:
                                bmp = wx.Bitmap("./resources/icon_in_qos_1_75.png", wx.BITMAP_TYPE_BMP)
                            if item.qos == 2:
                                bmp = wx.Bitmap("./resources/icon_in_qos_2_75.png", wx.BITMAP_TYPE_BMP)
                        else:
                            if item.qos == 0:
                                bmp = wx.Bitmap("./resources/icon_out_qos_0_75.png", wx.BITMAP_TYPE_BMP)
                            if item.qos == 1:
                                bmp = wx.Bitmap("./resources/icon_out_qos_1_75.png", wx.BITMAP_TYPE_BMP)
                            if item.qos == 2:
                                bmp = wx.Bitmap("./resources/icon_out_qos_2_75.png", wx.BITMAP_TYPE_BMP)
                    else:
                        if item.incoming:
                            if item.qos == 0:
                                bmp = wx.Bitmap("./resources/icon_in_qos_0_75.bmp", wx.BITMAP_TYPE_BMP)
                            if item.qos == 1:
                                bmp = wx.Bitmap("./resources/icon_in_qos_1_75.bmp", wx.BITMAP_TYPE_BMP)
                            if item.qos == 2:
                                bmp = wx.Bitmap("./resources/icon_in_qos_2_75.bmp", wx.BITMAP_TYPE_BMP)
                        else:
                            if item.qos == 0:
                                bmp = wx.Bitmap("./resources/icon_out_qos_0_75.bmp", wx.BITMAP_TYPE_BMP)
                            if item.qos == 1:
                                bmp = wx.Bitmap("./resources/icon_out_qos_1_75.bmp", wx.BITMAP_TYPE_BMP)
                            if item.qos == 2:
                                bmp = wx.Bitmap("./resources/icon_out_qos_2_75.bmp", wx.BITMAP_TYPE_BMP)

                    self.imageCtrl = wx.StaticBitmap(self.list, wx.ID_ANY, wx.Bitmap(bmp))
                    self.list.SetItemWindow(i, 1, self.imageCtrl)
                    if (i % 2) == 0:
                        self.list.SetItemBackgroundColour(i, wx.Colour(255, 255, 255))
                    else:
                        self.list.SetItemBackgroundColour(i, wx.Colour(224, 224, 224))
                    i += 1

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panelText, wx.EXPAND | wx.ALL, border=0)
        sizer.Add((0, 0), 0)
        sizer.Add(panelList, wx.EXPAND | wx.ALL, border=0)

        topPanel.SetSizer(sizer)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        vbox.Fit(self)
        self.Layout()
        self.SetSizer(vbox)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

class SendPanel(wx.Panel):
    def __init__(self, parent, app):
        self.app = app

        wx.Panel.__init__(self, parent)
        self.parent = parent

        #self.timer = wx.Timer(self, 1)
        #self.count = 0
        #self.gauge = wx.Gauge(self, 100, size=(359, 5))
        #self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        topPanel = wx.Panel(self, size=wx.Size(360, 560))
        #topPanel.SetBackgroundColour((255, 0, 0))
        panelText = wx.Panel(self, -1, size=wx.Size(360, 20))
        childPanel = wx.Panel(self, size=wx.Size(360, 400))
        childPanel.SetBackgroundColour((255, 255, 255))

        panelContent = wx.Panel(self, -1, size=wx.Size(360, 30))
        panelContent.SetBackgroundColour((255, 255, 255))
        panelName = wx.Panel(self, -1, size=wx.Size(360, 30))
        panelName.SetBackgroundColour((224, 224, 224))
        panelQos = wx.Panel(self, -1, size=wx.Size(360, 30))
        panelQos.SetBackgroundColour((255, 255, 255))
        panelRet = wx.Panel(self, -1, size=wx.Size(360, 30))
        panelRet.SetBackgroundColour((224, 224, 224))
        panelDup = wx.Panel(self, -1, size=wx.Size(360, 30))
        panelDup.SetBackgroundColour((255, 255, 255))
        panelButton = wx.Panel(self, -1, size=wx.Size(359, 50))

        text = MyStaticText(panelText, -1, ' send new message:', size=wx.Size(360, 20))
        textBox = wx.BoxSizer(wx.HORIZONTAL)
        textBox.Add(text)
        panelText.SetSizer(textBox)

        imgSettings = wx.Image("./resources/settings.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlContent = wx.StaticBitmap(panelContent, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.contentLabel = wx.StaticText(panelContent, -1, "Content:")
        self.contentText = wx.TextCtrl(panelContent, size=wx.Size(170, 30))
        contentBox = wx.BoxSizer(wx.HORIZONTAL)
        contentBox.AddSpacer(10)
        contentBox.Add(self.imageCtrlContent, 0, wx.CENTER)
        contentBox.AddSpacer(20)
        contentBox.Add(self.contentLabel, 0, wx.CENTER)
        contentBox.AddSpacer(60)
        contentBox.Add(self.contentText, 1, wx.ALIGN_RIGHT)
        panelContent.SetSizer(contentBox)

        self.imageCtrlName = wx.StaticBitmap(panelName, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.nameLabel = wx.StaticText(panelName, -1, "Topic:")
        self.nameText = wx.TextCtrl(panelName, size=wx.Size(170, 30))
        nameBox = wx.BoxSizer(wx.HORIZONTAL)
        nameBox.AddSpacer(10)
        nameBox.Add(self.imageCtrlName, 0, wx.CENTER)
        nameBox.AddSpacer(20)
        nameBox.Add(self.nameLabel, 0, wx.CENTER)
        nameBox.AddSpacer(80)
        nameBox.Add(self.nameText, 1, wx.ALIGN_RIGHT)
        panelName.SetSizer(nameBox)

        self.imageCtrlqos = wx.StaticBitmap(panelQos, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.qosLabel = wx.StaticText(panelQos, -1, "QoS:")
        self.comboQos = wx.ComboBox(panelQos, -1, '0', choices=qos)
        qosBox = wx.BoxSizer(wx.HORIZONTAL)
        qosBox.AddSpacer(10)
        qosBox.Add(self.imageCtrlqos, 0, wx.CENTER)
        qosBox.AddSpacer(20)
        qosBox.Add(self.qosLabel, 0, wx.CENTER)
        qosBox.AddSpacer(200)
        qosBox.Add(self.comboQos, 1, wx.CENTER)
        panelQos.SetSizer(qosBox)

        self.imageCtrlret = wx.StaticBitmap(panelRet, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.retLabel = wx.StaticText(panelRet, -1, "Retain:")
        self.retCheck = wx.CheckBox(panelRet)
        retainBox = wx.BoxSizer(wx.HORIZONTAL)
        retainBox.AddSpacer(10)
        retainBox.Add(self.imageCtrlret, 0, wx.CENTER)
        retainBox.AddSpacer(20)
        retainBox.Add(self.retLabel, 0, wx.CENTER)
        retainBox.AddSpacer(220)
        retainBox.Add(self.retCheck, 1, wx.CENTER)
        panelRet.SetSizer(retainBox)

        self.imageCtrldub = wx.StaticBitmap(panelDup, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.dubLabel = wx.StaticText(panelDup, -1, "Duplicate:")
        self.dubCheck = wx.CheckBox(panelDup)
        duplBox = wx.BoxSizer(wx.HORIZONTAL)
        duplBox.AddSpacer(10)
        duplBox.Add(self.imageCtrldub, 0, wx.CENTER)
        duplBox.AddSpacer(20)
        duplBox.Add(self.dubLabel, 0, wx.CENTER)
        duplBox.AddSpacer(199)
        duplBox.Add(self.dubCheck, 1, wx.CENTER)
        panelDup.SetSizer(duplBox)

        self.btnSend = wx.Button(panelButton, label="Send", size=wx.Size(350, 50), style = wx.NO_BORDER)
        self.btnSend.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.btnSend.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnSend.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.OnSend, self.btnSend)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        btnBox.Add(self.btnSend)
        panelButton.SetSizer(btnBox)

        #vbox.Add(self.gauge, wx.ALIGN_LEFT)
        #vbox.Add((0, 10), 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panelText, wx.EXPAND | wx.ALL, border=0)
        #sizer.Add((0, 10), 0)
        sizer.Add(panelContent, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelName, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelQos, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelRet, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelDup, wx.EXPAND | wx.ALL, border=0)
        sizer.Add((0, 230), 0)
        #sizer.Add(panelButton, wx.EXPAND | wx.ALL, border=0)
        childPanel.SetSizer(sizer)

        sizerTop = wx.BoxSizer(wx.VERTICAL)
        sizerTop.Add(panelText, wx.EXPAND | wx.ALL, border=0)
        sizerTop.Add(childPanel, wx.EXPAND | wx.ALL, border=0)
        sizerTop.Add(panelButton, wx.EXPAND | wx.ALL, border=0)

        topPanel.SetSizer(sizerTop)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        vbox.Fit(self)
        self.Layout()
        self.SetSizer(vbox)

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("./resources/iot_broker_background.png")
        dc.DrawBitmap(bmp, 0, 0)

    def OnSend(self, event):

        datamanage = datamanager()
        content = str.encode(self.contentText.GetValue())
        name = self.nameText.GetValue()
        qos = self.comboQos.GetValue()
        retain = self.retCheck.GetValue()
        dup = self.dubCheck.GetValue()

        self.contentText.SetValue('')
        self.nameText.SetValue('')
        self.comboQos.SetValue('0')
        self.retCheck.SetValue(False)
        self.dubCheck.SetValue(False)

        # SEND PUBLISH _________________________________________________________________________________SEND PUBLISH
        contentDecoded = content.decode('utf8')
        self.app.client.publish(name, int(qos), contentDecoded, retain, dup)
        #if int(qos)>0 and int(qos)<3:
            #self.timer.Start(1)

        if int(qos) == 0:
            # ADD to DB
            datamanage = datamanager()
            account = datamanage.get_default_account()
            if account.protocol != 3:
                message = MessageEntity(content=content, qos=int(qos), topicName=name,
                                        incoming=False, isRetain=retain, isDub=dup, accountentity_id=account.id)
                datamanage.add_entity(message)

        self.parent.DeletePage(3)
        self.parent.DeletePage(2)
        self.parent.AddPage(MessagesPanel(self.parent, self.app), "messages", imageId=2)
        self.parent.AddPage(LogoutPanel(self.parent, self.app), "logout", imageId=3)

    def OnTimer(self, event):
        self.count = self.count+1
        time.sleep(0.03)
        self.gauge.SetValue(self.count)
        self.gauge.Update()

        if self.count == 100:
            self.timer.Stop()
            self.count = 0
            self.gauge.SetValue(self.count)
            self.gauge.Update()

            #print("Puback is not received. Please, check state of your connection to server")
            wx.MessageBox('Puback or Unsuback is not received. Please, check state of your connection to server',
                          'Warning',wx.OK | wx.ICON_WARNING)
#GUI---------------------------------------------------------------------------------------------------------------------GUI

protocols = ['mqtt', 'mqttsn', 'coap', 'AMQP']
qos = ['0', '1', '2']

switch_protocol = {
            'mqtt': 1,
            'mqttsn': 2,
            'coap': 3,
            'AMQP': 4
        }

switch_incoming = {
            True : 'In',
            False: 'Out'
        }

switch_MQTTmessageType = {
    1 : 'MQ_CONNECT',
    2 : 'MQ_CONNACK',
    3 : 'MQ_PUBLISH',
    4 : 'MQ_PUBACK',
    5 : 'MQ_PUBREC',
    6 : 'MQ_PUBREL',
    7 : 'MQ_PUBCOMP',
    8 : 'MQ_SUBSCRIBE',
    9 : 'MQ_SUBACK',
    10 : 'MQ_UNSUBSCRIBE',
    11 : 'MQ_UNSUBACK',
    12 : 'MQ_PINGREQ',
    13 : 'MQ_PINGRESP',
    14 : 'MQ_DISCONNECT'
        }

from venv.iot.classes.UIClient import *

class MyApp(wx.App, UIClient):
    def OnInit(self):
        self.gui = self
        self.client = None
        #self.frame = LoadingForm(None, -1, "Loading", self)
        self.frame = MainForm(None, -1, "Main", self)
        #self.frame = LoginForm(None, -1, "Login", self)
        self.frame.Show(True)
        datamanage = datamanager()
        datamanage.create_db()
        datamanage.clear()
        datamanage.clear_default_account()
        return True

    def timeout(self):
        print("GUI timeout")

    def connackReceived(self, returnCode):
        #print('App connackReceived')
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def publishReceived(self, topic, qos, content, dup, retainFlag):
        print('App publishReceived')
        #store Message
        datamanage = datamanager()
        account = datamanage.get_default_account()

        if isinstance(topic, FullTopic):
            topicName = topic.getValue()
        else:
            topicName = topic.getName()

        message = MessageEntity(content = bytes(content, encoding='utf_8'), qos = qos.getValue(), topicName = topicName,
                                incoming = True, isRetain = retainFlag, isDub = dup, accountentity_id = account.id)
        datamanage.add_entity(message)
        #print('Message stored to DB ' + str(message))
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def pubackReceived(self, topic, qos, content, dup, retainFlag, returnCode):
        print('App pubackReceived')
        # store Message
        datamanage = datamanager()
        account = datamanage.get_default_account()

        if isinstance(topic, FullTopic):
            topicName = topic.getValue()
        else:
            topicName = topic.getName()

        #print(' topicName=' + str(topicName))
        message = MessageEntity(content=bytes(content, encoding='utf_8'), qos=qos.getValue(), topicName=topicName,
                                incoming=False, isRetain=retainFlag, isDub=dup, accountentity_id=account.id)
        datamanage.add_entity(message)
        #print('App pubackReceived entity was saved')
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def subackReceived(self, topic, qos, returnCode):
        #print('App subackReceived' + str(topic) + ' ' + str(qos))
        #store topic
        datamanage = datamanager()
        account = datamanage.get_default_account()
        if isinstance(topic, MQTopic):
            topicToDB = TopicEntity(topicName = topic.getName(), qos=qos.getValue(), accountentity_id = account.id)
            datamanage.add_entity(topicToDB)

    def unsubackReceived(self, listTopics):
        #print('App unsubackReceived')
        #delete topics from list
        datamanage = datamanager()
        for name in listTopics:
            datamanage.delete_topic_name(name)
            #print('Topic deleted from DB ' + str(name))
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def pingrespReceived(self):
        #print('MyApp pingresp Received')
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def disconnectReceived(self):
        #print('MyApp disconnectReceived')
        pass

    def errorReceived(self, text):
        #print('MyApp errorReceived: ' + text)
        pass

log.startLogging(sys.stdout)

app = MyApp(0)
reactor.registerWxApp(app)

#start the event loop
reactor.run()