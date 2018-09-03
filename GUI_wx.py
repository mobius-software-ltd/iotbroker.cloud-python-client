import wx
import time
import sys

from database import AccountEntity, TopicEntity, MessageEntity, Base, datamanager
from venv.IoT.Classes.AccountValidation import  *

from twisted.python import log
from twisted.internet import wxreactor
#FOR ALERTS
import pymsgbox
#pymsgbox.alert('Please, select account','Account selection is empty Error')

from wx.lib.agw import ultimatelistctrl as ULC

wxreactor.install()

#import t.i.reactor only after installing wxreactor
from twisted.internet import reactor

from venv.IoT.MQTT.MQTTclient import *

#GUI---------------------------------------------------------------------------------------------------------------------GUI
class LoadingForm(wx.Frame):
    def __init__(self, parent, ID, title, app):
        self.app = app
        wx.Frame.__init__(self, parent, ID, title,size=wx.Size(360,500))
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
            print("timer stopped")

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
                    print('Protocol= ' + str(protocols[account.protocol-1]))

                if account.protocol == 3:
                    print('Protocol= ' + str(protocols[account.protocol-1]))

                if account.protocol == 4:
                    print('Protocol= ' + str(protocols[account.protocol-1]))

            else:
                print("show AccountsForm")
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

        self.text = wx.Button(panelText, label="Please select account", size=wx.Size(360, 50))
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

        bmp = wx.Bitmap("./resources/ic_delete_with_background.png", wx.BITMAP_TYPE_BMP)

        i = 0
        if len(accounts) > 0:
            for item in accounts:
                self.btnDel = wx.BitmapButton(self.list, id=i, bitmap=bmp,
                                              size=(bmp.GetWidth() + 12, bmp.GetHeight() + 10), style = wx.NO_BORDER)
                self.Bind(wx.EVT_BUTTON, self.OnDelete, self.btnDel)
                self.list.InsertStringItem(i, str(item.username)+'\n'+ str(item.clientID) +'\n'+ str(item.serverHost + ":" + str(item.port)))
                self.list.SetItemWindow(i, 1, self.btnDel)
                i += 1

        self.btnCreate = wx.Button(panelBtn, label="CREATE", size=wx.Size(360, 50))
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
        account = datamanage.set_default_account_clientID(clientID)
        self.Hide()
        next = LoadingForm(None, -1, "Loading", self.app)
        next.Show()

    def OnDelete(self, event):
        btn = event.GetEventObject()
        id = btn.GetId()
        accountID = id
        datamanage = datamanager()
        account = datamanage.delete_account(accountID)
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
        self.comboProtocol = wx.ComboBox(panel1, -1, 'MQTT', choices=protocols)

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
        protocol_horizontal.AddSpacer(100)
        protocol_horizontal.Add(self.comboProtocol, 1, wx.RIGHT, 20)

        username_horizontal.AddSpacer(10)
        username_horizontal.Add(self.imageCtrlName, wx.LEFT, 20)
        username_horizontal.AddSpacer(10)
        username_horizontal.Add(self.nameLabel)
        username_horizontal.AddSpacer(50)
        username_horizontal.Add(self.nameText, 1, wx.RIGHT, 20)

        pasw_horizontal.AddSpacer(10)
        pasw_horizontal.Add(self.imageCtrlPasw, wx.LEFT, 20)
        pasw_horizontal.AddSpacer(10)
        pasw_horizontal.Add(self.paswLabel)
        pasw_horizontal.AddSpacer(52)
        pasw_horizontal.Add(self.paswText, 1, wx.RIGHT, 20)

        clientId_horizontal.AddSpacer(10)
        clientId_horizontal.Add(self.imageCtrlclient, wx.LEFT, 20)
        clientId_horizontal.AddSpacer(10)
        clientId_horizontal.Add(self.idLabel)
        clientId_horizontal.AddSpacer(60)
        clientId_horizontal.Add(self.idText, 1, wx.RIGHT, 20)

        host_horizontal.AddSpacer(10)
        host_horizontal.Add(self.imageCtrlhost, wx.LEFT, 20)
        host_horizontal.AddSpacer(10)
        host_horizontal.Add(self.hostLabel)
        host_horizontal.AddSpacer(50)
        host_horizontal.Add(self.hostText, 1, wx.RIGHT, 20)

        port_horizontal.AddSpacer(10)
        port_horizontal.Add(self.imageCtrlport, wx.LEFT, 20)
        port_horizontal.AddSpacer(10)
        port_horizontal.Add(self.portLabel)
        port_horizontal.AddSpacer(100)
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
        clean_horizontal.AddSpacer(150)
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
        retain_horizontal.AddSpacer(210)
        retain_horizontal.Add(self.retainCheck, 1, wx.RIGHT, 20)

        qos_horizontal.AddSpacer(10)
        qos_horizontal.Add(self.imageCtrlqos)
        qos_horizontal.AddSpacer(10)
        qos_horizontal.Add(self.qosLabel)
        qos_horizontal.AddSpacer(200)
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
        self.btn = wx.Button(topPanel, label="Log In", size=wx.Size(360, 50))
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
            pymsgbox.alert('Please, fill in all required fileds: Username, Password, ClientID, Host, Port, Keepalive ', 'Account creation Error')

    def onClose(self, event):
        if self.app.client is not None:
            self.app.client.timers.stopAllTimers()
        reactor.stop()

def getNextImageID(count):
    imID = 0
    while True:
        yield imID

        imID += 1
    # end while
# end def

class ToolbookImpl(wx.Toolbook):

    def __init__(self, parent, app):
        wx.Toolbook.__init__(self, parent, wx.ID_ANY, style=wx.BK_DEFAULT | wx.BK_BOTTOM)
        # Make an image list using the LBXX images
        self.parent = parent
        il = wx.ImageList(75, 41)
        tlist_img = wx.Bitmap("./resources/ic_topics_list_blue_75.png")
        send_img = wx.Bitmap("./resources/is_message_list_blue-1_75.png")
        mlist_img = wx.Bitmap("./resources/is_message_list_blue-03_75.png")
        logout_img = wx.Bitmap("./resources/logout_75.png")

        il.Add(tlist_img)
        il.Add(send_img)
        il.Add(mlist_img)
        il.Add(logout_img)
        self.AssignImageList(il)
        imageIdGenerator = getNextImageID(il.GetImageCount())

        notebookPageList = [(TopicsPanel(self, app), 'topics'),
                            (SendPanel(self, app), 'send'),
                            (MessagesPanel(self, app), 'messages'),
                            (LogoutPanel(self, app), 'logout')]
        for page, label in notebookPageList:
            self.AddPage(page, label, imageId=imageIdGenerator.__next__())

        self.ChangeSelection(1)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)

    def OnPageChanging(self, event):
        new = event.GetSelection()
        #print('cur page: ' + str(new))
        if new == 3:
            self.parent.Hide()
            next = AccountsForm(None, 1, "Accounts List", self.parent.app)
            next.Show()
            #______________________________________________________________________SEND___DISCONNECT
            if self.parent.app.client is not None:
                self.parent.app.client.disconnectWith()
        event.Skip()

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        #print('cur page: ' + str(new))
        event.Skip()

class MainForm(wx.Frame):
    def __init__(self, parent, ID, title, app):
        wx.Frame.__init__(self, parent, ID, title, size=wx.Size(370, 560))
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
        print('LOGOUT')

class TopicsPanel(wx.Panel):
    def __init__(self, parent, app):

        self.app = app
        wx.Panel.__init__(self, parent)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)
        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        topPanel = wx.Panel(self, size=wx.Size(360, 560))
        panelText = wx.Panel(self, -1, size=wx.Size(360, 20))
        panelList = wx.Panel(self, -1, size=wx.Size(360, 300))
        panelTopic = wx.Panel(self, -1, size=wx.Size(360, 80))
        panelTopic.SetBackgroundColour((255, 255, 255))
        panelBtn = wx.Panel(self, -1, size=wx.Size(360, 50))

        text = wx.StaticText(panelText, -1, "  topics list:",size=wx.Size(360, 50))
        text.SetFont(boldfont)

        self.list = ULC.UltimateListCtrl(panelList, wx.ID_ANY, agwStyle=ULC.ULC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.list.SetFont(boldfont)

        self.list.InsertColumn(0, "Topic")
        self.list.InsertColumn(1, "Qos")
        self.list.InsertColumn(2, "Button")

        self.list.SetColumnWidth(0, 250)
        self.list.SetColumnWidth(1, 50)
        self.list.SetColumnWidth(2, 50)

        self.list.SetSize(350, 300)

        datamanage = datamanager()
        account = datamanage.get_default_account()
        self.list.SetFont(font)

        bmp = wx.Bitmap("./resources/ic_delete_with_background.png", wx.BITMAP_TYPE_BMP)
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

                    qosBmp = wx.Bitmap("./resources/icon_qos_0_75.png", wx.BITMAP_TYPE_BMP)
                    if item.qos == 1:
                        qosBmp = wx.Bitmap("./resources/icon_qos_1_75.png", wx.BITMAP_TYPE_BMP)
                    if item.qos == 2:
                        qosBmp = wx.Bitmap("./resources/icon_qos_2_75.png", wx.BITMAP_TYPE_BMP)

                    self.imageCtrlQos = wx.StaticBitmap(self.list, wx.ID_ANY, wx.Bitmap(qosBmp))
                    self.list.SetItemWindow(i, 1, self.imageCtrlQos)
                    self.list.SetItemWindow(i, 2, self.btnDel)
                    i += 1

        self.btnCreate = wx.Button(topPanel, label="Add", size=wx.Size(359, 50))
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
        panelTopic_vertical.AddSpacer(5)
        panelTopic_vertical.Add(topic_horizontal)
        panelTopic_vertical.AddSpacer(5)
        panelTopic_vertical.Add(qos_horizontal)

        panelTopic.SetSizer(panelTopic_vertical)

        sizer.Add(panelText, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelList, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelTopic, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(self.btnCreate, wx.EXPAND | wx.ALL, border=0)

        topPanel.SetSizer(sizer)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        vbox.Fit(self)
        self.Layout()
        self.SetSizer(vbox)

    def OnCreate(self, event):
        name = self.nameText.GetValue()
        qos = self.comboQos.GetValue()
        #ADD to list

        self.nameText.SetValue('');
        self.comboQos.SetValue('0');

        i = self.list.GetItemCount()
        bmp = wx.Bitmap("./resources/ic_delete_with_background.png", wx.BITMAP_TYPE_BMP)
        self.btnDel = wx.BitmapButton(self.list, id=i, bitmap=bmp,
                                      size=(bmp.GetWidth() + 12, bmp.GetHeight() + 10), style=wx.NO_BORDER)

        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.btnDel)
        self.list.InsertStringItem(i, str(name))
        qosBmp = wx.Bitmap("./resources/icon_qos_0_75.png", wx.BITMAP_TYPE_BMP)
        if int(qos) == 1:
            qosBmp = wx.Bitmap("./resources/icon_qos_1_75.png", wx.BITMAP_TYPE_BMP)
        if int(qos) == 2:
            qosBmp = wx.Bitmap("./resources/icon_qos_2_75.png", wx.BITMAP_TYPE_BMP)
        self.imageCtrlQos = wx.StaticBitmap(self.list, wx.ID_ANY, wx.Bitmap(qosBmp))

        self.list.SetItemWindow(i, 1, self.imageCtrlQos)
        self.list.SetItemWindow(i, 2, self.btnDel)
        # SEND SUBSCRIBE _________________________________________________________________________________SEND SUBSCRIBE
        self.app.client.subscribeTo(name, int(qos))


    def OnDelete(self, event):
        btn = event.GetEventObject()
        id = btn.GetId()
        topicName = self.list.GetItem(id, 0).GetText()
        # SEND UNSUBSCRIBE _________________________________________________________________________________SEND UNSUBSCRIBE
        self.app.client.unsubscribeFrom(topicName)

class MessagesPanel(wx.Panel):
    def __init__(self, parent, app):
        self.app = app
        wx.Panel.__init__(self, parent)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)
        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        topPanel = wx.Panel(self, size=wx.Size(360, 560))
        panelText = wx.Panel(self, -1, size=wx.Size(360, 20))
        panelList = wx.Panel(self, -1, size=wx.Size(360, 420))

        text = wx.StaticText(panelText, -1, "  messages list:", size=wx.Size(360, 50))
        text.SetFont(boldfont)

        self.list = ULC.UltimateListCtrl(panelList, wx.ID_ANY,
                                         agwStyle=ULC.ULC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        self.list.SetFont(boldfont)
        self.list.InsertColumn(0, "Topic")
        self.list.InsertColumn(1, "Qos")

        self.list.SetColumnWidth(0, 280)
        self.list.SetColumnWidth(1, 59)

        self.list.SetSize(350, 420)

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
                    self.imageCtrl = wx.StaticBitmap(self.list, wx.ID_ANY, wx.Bitmap(bmp))
                    self.list.SetItemWindow(i, 1, self.imageCtrl)
                    i += 1

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panelText, wx.EXPAND | wx.ALL, border=0)
        sizer.Add(panelList, wx.EXPAND | wx.ALL, border=0)

        topPanel.SetSizer(sizer)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topPanel)
        vbox.Fit(self)
        self.Layout()
        self.SetSizer(vbox)

class SendPanel(wx.Panel):
    def __init__(self, parent, app):
        self.app = app

        wx.Panel.__init__(self, parent)
        self.parent = parent

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)

        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)

        text = wx.StaticText(self, -1, "  send new message:", size=wx.Size(360, 20))
        text.SetFont(boldfont)

        imgSettings = wx.Image("./resources/settings.png", wx.BITMAP_TYPE_ANY)
        imgSettings = imgSettings.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.imageCtrlContent = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.contentLabel = wx.StaticText(self, -1, "Content:")
        self.contentText = wx.TextCtrl(self, size=wx.Size(150, 30))

        self.imageCtrlName = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.nameLabel = wx.StaticText(self, -1, "topicName:")
        self.nameText = wx.TextCtrl(self, size=wx.Size(150, 30))

        self.imageCtrlqos = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.qosLabel = wx.StaticText(self, -1, "QoS:")
        self.comboQos = wx.ComboBox(self, -1, '0', choices=qos)

        self.imageCtrlret = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.retLabel = wx.StaticText(self, -1, "Retain:")
        self.retCheck = wx.CheckBox(self)

        self.imageCtrldub = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(imgSettings))
        self.dubLabel = wx.StaticText(self, -1, "Duplicate:")
        self.dubCheck = wx.CheckBox(self)

        self.btnSend = wx.Button(self, label="Send", size=wx.Size(360, 50))
        self.btnSend.SetBackgroundColour(wx.Colour(30, 144, 255))
        self.btnSend.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.btnSend.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.OnSend, self.btnSend)

        hbox1.AddSpacer(30)
        hbox1.Add(self.imageCtrlContent)
        hbox1.AddSpacer(20)
        hbox1.Add(self.contentLabel)
        hbox1.AddSpacer(60)
        hbox1.Add(self.contentText, 1, wx.ALIGN_RIGHT)

        hbox2.AddSpacer(30)
        hbox2.Add(self.imageCtrlName)
        hbox2.AddSpacer(20)
        hbox2.Add(self.nameLabel)
        hbox2.AddSpacer(40)
        hbox2.Add(self.nameText, 1, wx.ALIGN_RIGHT)

        hbox3.AddSpacer(30)
        hbox3.Add(self.imageCtrlqos)
        hbox3.AddSpacer(20)
        hbox3.Add(self.qosLabel)
        hbox3.AddSpacer(180)
        hbox3.Add(self.comboQos, 1, wx.ALIGN_RIGHT)

        hbox5.AddSpacer(30)
        hbox5.Add(self.imageCtrlret)
        hbox5.AddSpacer(20)
        hbox5.Add(self.retLabel)
        hbox5.AddSpacer(200)
        hbox5.Add(self.retCheck, 1, wx.ALIGN_RIGHT)

        hbox6.AddSpacer(30)
        hbox6.Add(self.imageCtrldub)
        hbox6.AddSpacer(20)
        hbox6.Add(self.dubLabel)
        hbox6.AddSpacer(180)
        hbox6.Add(self.dubCheck, 1, wx.ALIGN_RIGHT)

        hbox7.Add(self.btnSend)

        vbox.Add(text)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_LEFT)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox2, 0, wx.ALIGN_LEFT)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox3, 0, wx.ALIGN_LEFT)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox5, 0, wx.ALIGN_LEFT)
        vbox.Add((0, 10), 0)
        vbox.Add(hbox6, 0, wx.ALIGN_LEFT)
        vbox.Add((0, 210), 0)
        vbox.Add(hbox7, 0, wx.ALIGN_CENTRE)

        self.SetSizer(vbox)
        self.Centre()

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

        if int(qos) == 0:
            # ADD to DB
            datamanage = datamanager()
            account = datamanage.get_default_account()
            message = MessageEntity(content=content, qos=int(qos), topicName=name,
                                    incoming=False, isRetain=retain, isDub=dup, accountentity_id=account.id)
            datamanage.add_entity(message)

            self.parent.DeletePage(3)
            self.parent.DeletePage(2)
            self.parent.AddPage(MessagesPanel(self.parent, self.app), "", imageId=2)
            self.parent.AddPage(LogoutPanel(self.parent, self.app), "", imageId=3)

#GUI---------------------------------------------------------------------------------------------------------------------GUI

protocols = ['MQTT', 'MQTT_SN', 'COAP', 'AMQP']
qos = ['0', '1', '2']

switch_protocol = {
            'MQTT': 1,
            'MQTT_SN': 2,
            'COAP': 3,
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

from venv.IoT.Classes.UIClient import *

class MyApp(wx.App, UIClient):
    def OnInit(self):
        self.gui = self
        self.client = None
        self.frame = LoadingForm(None, -1, "Loading", self)
        self.frame.Show(True)
        datamanage = datamanager()
        datamanage.create_db()
        datamanage.clear()
        return True

    def timeout(self):
        print("GUI timeout")

    def connackReceived(self, returnCode):
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def publishReceived(self, topic, qos, content, dup, retainFlag):
        print('App publishReceived')
        #store Message
        datamanage = datamanager()
        account = datamanage.get_default_account()
        message = MessageEntity(content = bytes(content, encoding='utf_8'), qos = qos.getValue(), topicName = topic.name, incoming = True, isRetain = retainFlag, isDub = dup, accountentity_id = account.id)
        datamanage.add_entity(message)
        print('Message stored to DB ' + str(message))
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def pubackReceived(self, topic, qos, content, dup, retainFlag, returnCode):
        print('App pubackReceived')
        # store Message
        datamanage = datamanager()
        account = datamanage.get_default_account()
        message = MessageEntity(content=bytes(content, encoding='utf_8'), qos=qos.getValue(), topicName=topic.name,
                                incoming=False, isRetain=retainFlag, isDub=dup, accountentity_id=account.id)
        datamanage.add_entity(message)
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def subackReceived(self, topic, qos, returnCode):
        print('App subackReceived')
        #store topic
        datamanage = datamanager()
        account = datamanage.get_default_account()
        topicToDB = TopicEntity(topicName = topic.name, qos=qos.getValue(), accountentity_id = account.id)
        datamanage.add_entity(topicToDB)

    def unsubackReceived(self, listTopics):
        print('App unsubackReceived')
        #delete topics from list
        datamanage = datamanager()
        for name in listTopics:
            datamanage.delete_topic_name(name)
            print('Topic deleted from DB ' + str(name))
        self.frame.Hide()
        self.frame = MainForm(None, -1, "Main", self)
        self.frame.Show()

    def pingrespReceived(self):
        print('MyApp pingresp Received')

    def disconnectReceived(self):
        print('MyApp disconnectReceived')

    def errorReceived(self, text):
        print('MyApp errorReceived: ' + text)

log.startLogging(sys.stdout)

app = MyApp(0)
reactor.registerWxApp(app)

#start the event loop
reactor.run()