try:
    import Tkinter as tk # this is for python2
    from Tkinter import *
    from Tkinter import ttk
    import Tkinter.messagebox as messagebox
    from PIL import ImageTk, Imag
except:
    import tkinter as tk # this is for python3
    from tkinter import *
    from tkinter import ttk
    from tkinter import font
    import tkinter.messagebox as messagebox
    from PIL import ImageTk, Image

from database import AccountEntity, TopicEntity, MessageEntity, Base, datamanager
from iot.classes.AccountValidation import *

from iot.mqtt.MQTTclient import *
from iot.mqttsn.MQTTSNclient import *
from iot.coap.CoapClient import *
from iot.websocket.WSclient import *
from iot.amqp.AMQPclient import *

from twisted.python import log
from twisted.internet import tksupport, reactor

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def center_child(win):
    win.update_idletasks()
    width = win.winfo_width() + 160
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height() + 300
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

class Loading:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.loading = tk.Toplevel()
        center_child(self.loading)
        self.loading.geometry("360x500")

        img = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        background = Label(master=self.loading, image=img, bd=0)
        background.pack(fill='both', expand=True)
        background.image = img

        # resize empty rows, columns to put other elements in center
        background.rowconfigure(0, weight=100)
        background.rowconfigure(3, weight=100)
        background.columnconfigure(0, weight=100)
        background.columnconfigure(3, weight=100)

        imgLogo = ImageTk.PhotoImage(Image.open("./resources/iotbroker_icon_big.png"))
        logo = Label(background, image=imgLogo, bd=0)
        logo.grid(row=0, column=1)
        logo.image = imgLogo

        imgTxt = ImageTk.PhotoImage(Image.open("./resources/ic_loading_text.png"))
        logoTxt = Label(background, image=imgTxt, bd=0)
        logoTxt.grid(row=1, column=1)
        logoTxt.image = imgTxt

        self.loading.progress = ttk.Progressbar(background, length=300, orient='horizontal', mode='determinate')
        self.loading.progress.grid(row=3, column=1)
        self.loading.progress.start(30)
        self.loading.after(3000, self.stop_progressbar)

    def stop_progressbar(self):
        self.loading.progress.stop()
        self.loading.progress.step(50)

        datamanage = datamanager()
        account = datamanage.get_default_account()
        self.loading.destroy()

        if account is not None:
            print('connection to: ' + account.serverHost + ":" + str(account.port))
            if account.cleanSession:
                datamanage.clear_by_id(account.id)

            if account.protocol == 1:
                self.app.client = MQTTclient(account, self.app)
                self.app.client.goConnect()

            if account.protocol == 2:
                self.app.client = MQTTSNclient(account, self.app)
                self.app.client.goConnect()

            if account.protocol == 3:
                self.app.client = CoapClient(account, self.app)
                self.app.client.goConnect()

            if account.protocol == 4:
                self.app.client = WSclient(account, self.app)
                self.app.client.goConnect()
                time.sleep(1.5)

            if account.protocol == 5:
                self.app.client = AMQPclient(account, self.app)
                self.app.client.goConnect()
        else:
            self.accounts = Accounts(self.root, self.app)
            self.accounts.start()

    def start(self):
        self.loading.wait_window()

class Accounts:

    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.accounts = tk.Toplevel()
        center_child(self.accounts)
        self.accounts.geometry("369x500")

        self.accounts.protocol("WM_DELETE_WINDOW", self.close)
        small_font = font.Font(family='Verdana', size=10, weight="normal")
        buttonColor = '#%02x%02x%02x' % (30, 144, 255)
        label = Label(self.accounts, text="Please select account", highlightthickness=0, bg=buttonColor, fg='white', height=4, width=52, font=small_font).grid(row=0)

        self.clientIDs = []
        gui_style = ttk.Style()
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', background='white', border=0, height=3, width=48, font=small_font)

        canvas = tk.Canvas(self.accounts, width=360, height=370, bg='white', highlightcolor='white')
        myframe = ttk.Frame(canvas,  style='My.TFrame')

        buttonImage = Image.open('./resources/ic_delete_with_background.png')
        self.buttonPhoto = ImageTk.PhotoImage(buttonImage)

        datamanage = datamanager()
        accounts = datamanage.get_accounts_all()

        i = 0
        if len(accounts) > 0:
            for item in accounts:
                text = ' {}\n {}\n {}:{}'.format(item.username, item.clientID, item.serverHost, item.port)
                self.clientIDs.append(item.clientID)
                txtButton = ttk.Button(myframe, text=text, style='My.TLabel', command=lambda x=i: self.connect(x)).grid(row=i+1)
                delButton = ttk.Button(myframe, image=self.buttonPhoto, text="Del", style='My.TLabel',command=lambda x=i: self.delete(x)).grid(row=i+1, column=1)
                i+=1

        canvas.create_window(0, 0, anchor='nw', window=myframe)
        #vbar = ttk.Scrollbar(myframe, orient='vertical', command=canvas.yview)

        canvas.grid(row=1, column=0, sticky='eswn')
        #vbar.grid(row=1, column=2)

        button = Button(self.accounts, text="Add", font=small_font, highlightthickness=0, bg=buttonColor, fg='white', activebackground=buttonColor, height=4, width=49, command=self.createAccount).grid(row=2)

    def close(self):
        self.accounts.destroy()
        reactor.callFromThread(reactor.stop)


    def createAccount(self):
        self.accounts.destroy()
        self.login = Login(self.root, self.app)
        self.login.start()

    def delete(self, id):
        clientID = self.clientIDs[id]
        datamanage = datamanager()
        account = datamanage.delete_account(clientID)
        self.accountsNew = Accounts(self.root, self.app)
        self.accounts.destroy()
        self.accountsNew.start()

    def connect(self, id):
        clientID = self.clientIDs[id]
        datamanage = datamanager()
        datamanage.clear_default_account()
        datamanage.set_default_account_clientID(clientID)

        self.accounts.destroy()
        loading = Loading(self.root, self.app)
        loading.start()

    def start(self):
        self.accounts.wait_window()

class Login:

    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.login = tk.Toplevel()
        center_child(self.login)
        self.login.geometry("360x627")

        self.login.protocol("WM_DELETE_WINDOW", self.close)

        buttonColor = '#%02x%02x%02x' % (30, 144, 255)
        small_font = font.Font(family='Verdana', size=10, weight="normal")
        bold_font = font.Font(family='Verdana', size=9, weight="bold")
        size = 34
        txtSize = 19

        self.varClean = BooleanVar()
        self.varEnabled = BooleanVar()

        gui_style = ttk.Style()
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, background='gray70', width=52)
        gui_style.configure('My.TCombobox', background='white', border=0)

        settingsImage = Image.open('./resources/settings34.png')
        self.settingsPhoto = ImageTk.PhotoImage(settingsImage)
        userImage = Image.open('./resources/username34.png')
        self.userPhoto = ImageTk.PhotoImage(userImage)
        paswImage = Image.open('./resources/password34.png')
        self.paswPhoto = ImageTk.PhotoImage(paswImage)
        idImage = Image.open('./resources/clienid34.png')
        self.idPhoto = ImageTk.PhotoImage(idImage)
        hostImage = Image.open('./resources/host34.png')
        self.hostPhoto = ImageTk.PhotoImage(hostImage)
        cleanImage = Image.open('./resources/cleansession34.png')
        self.cleanPhoto = ImageTk.PhotoImage(cleanImage)
        keepImage = Image.open('./resources/keepalive34.png')
        self.keepPhoto = ImageTk.PhotoImage(keepImage)

        regImage = Image.open('./resources/regInfo.png')
        self.regPhoto = ImageTk.PhotoImage(regImage)

        whitebg = 'white'
        graybg = 'gray92'
        heightLabel = 3
        widthLabel = 25

        regInfo = ttk.Label(self.login, text=" registration info:", style='My.TLabel').grid(row=0, sticky='w')
        #regInfo = Label(self.login, image=self.regPhoto).grid(row=0, sticky='w')
        regCanvas = tk.Canvas(self.login, width=359, height=210, bg=whitebg, highlightcolor=whitebg)
        regFrame = ttk.Frame(regCanvas, style='My.TFrame')
        regCanvas.create_window(0, 0, anchor='nw', window=regFrame)

        #Protocol line
        protocolImg = Label(master=regFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        protocolLabel = Label(master=regFrame, text='   Protocol:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=0, column=1, sticky='w')
        self.comboProtocol = ttk.Combobox(master=regFrame, values=protocols, width=10, style='My.TCombobox')
        self.comboProtocol.current(0)
        self.comboProtocol.grid(row=0, column=2, sticky='e')

        # Username line
        userImg = Label(master=regFrame, image=self.userPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        userLabel = Label(master=regFrame, text='   Username:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg).grid(row=1, column=1, sticky='w')
        self.nameText = Entry(master=regFrame, width=txtSize, font=small_font, bg=graybg)
        self.nameText.grid(row=1, column=2, sticky='w')

        # Password line
        paswImg = Label(master=regFrame, image=self.paswPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2,column=0)
        paswLabel = Label(master=regFrame, text='   Password:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=2, column=1, sticky='w')
        self.paswText = Entry(master=regFrame, width=txtSize, font=small_font, bg=whitebg, show=False)
        self.paswText.grid(row=2, column=2)

        # ClientID line
        idImg = Label(master=regFrame, image=self.idPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=3,column=0)
        idLabel = Label(master=regFrame, text='   Client ID:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg).grid(row=3, column=1, sticky='w')
        self.idText = Entry(master=regFrame, width=txtSize, font=small_font, bg=graybg)
        self.idText.grid(row=3, column=2)

        # Host line
        hostImg = Label(master=regFrame, image=self.hostPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=4, column=0)
        hostLabel = Label(master=regFrame, text='   Server host:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(
            row=4, column=1, sticky='w')
        self.hostText = Entry(master=regFrame, width=txtSize, font=small_font, bg=whitebg)
        self.hostText.grid(row=4, column=2)

        # Port line
        portImg = Label(master=regFrame, image=self.hostPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=5,column=0)
        portLabel = Label(master=regFrame, text='   Port:', bd=0, height=heightLabel, width=widthLabel, anchor="w",bg=graybg).grid(row=5, column=1, sticky='w')
        self.portText = Entry(master=regFrame, width=txtSize, font=small_font, bg=graybg)
        self.portText.grid(row=5, column=2)

        regCanvas.grid(row=1, sticky='eswn')

        settingsInfo = ttk.Label(self.login, text=" settings:", style='My.TLabel').grid(row=2, sticky='w')
        setCanvas = tk.Canvas(self.login, width=359, height=210, bg=whitebg, highlightcolor=whitebg)
        setFrame = ttk.Frame(setCanvas, style='My.TFrame')
        setCanvas.create_window(0, 0, anchor='nw', window=setFrame)

        # Clean line
        portImg = Label(master=setFrame, image=self.cleanPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0,column=0)
        portLabel = Label(master=setFrame, text='   Clean session:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=0, column=1)
        self.cleanCheck = Checkbutton(master=setFrame, width=txtSize-2, variable=self.varClean, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.cleanCheck.grid(row=0, column=2)

        # Keepalive line
        keepImg = Label(master=setFrame, image=self.keepPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1,column=0)
        keepLabel = Label(master=setFrame, text='   Keepalive:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg).grid(row=1, column=1)
        self.keepText = Entry(master=setFrame, width=txtSize, font=small_font, bg=graybg)
        self.keepText.grid(row=1, column=2)

        # Will line
        willImg = Label(master=setFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2, column=0)
        willLabel = Label(master=setFrame, text='   Will:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=2, column=1)
        self.willText = Entry(master=setFrame, width=txtSize, font=small_font, bg=whitebg)
        self.willText.grid(row=2, column=2)

        # Will topic line
        keepImg = Label(master=setFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=3,column=0)
        keepLabel = Label(master=setFrame, text='   Will topic:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg).grid(row=3, column=1)
        self.willTText = Entry(master=setFrame, width=txtSize, font=small_font, bg=graybg)
        self.willTText.grid(row=3, column=2)

        # Retain line
        retImg = Label(master=setFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=5,column=0)
        retLabel = Label(master=setFrame, text='   Retain:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg).grid(row=5, column=1)
        self.retainCheck = Checkbutton(master=setFrame, width=txtSize - 2, height=2, bd=0, anchor='e', bg=graybg, activebackground=graybg, highlightbackground=graybg, highlightthickness=0)
        self.retainCheck.grid(row=5, column=2)

        # QoS line
        qosImg = Label(master=setFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=4, column=0)
        qosLabel = Label(master=setFrame, text='   QoS:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=4, column=1)
        self.comboQos = ttk.Combobox(master=setFrame, values=qos, width=10, style='My.TCombobox')
        self.comboQos.current(0)
        self.comboQos.grid(row=4, column=2, sticky='e')

        setCanvas.grid(row=3, sticky='eswn')

        security = ttk.Label(self.login, text=" security:", style='My.TLabel').grid(row=4, sticky='w')
        secCanvas = tk.Canvas(self.login, width=359, height=100, bg=whitebg, highlightcolor=whitebg)
        secFrame = ttk.Frame(secCanvas, style='My.TFrame')
        secCanvas.create_window(0, 0, anchor='nw', window=secFrame)

        # Enable line
        enableImg = Label(master=secFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        enableLabel = Label(master=secFrame, text='   Enabled:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=0, column=1)
        self.enabledCheck = Checkbutton(master=secFrame, width=txtSize - 2, variable=self.varEnabled, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.enabledCheck.grid(row=0, column=2)

        # Certificate line
        certImg = Label(master=secFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        certLabel = Label(master=secFrame, text='   Certificate:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg).grid(row=1, column=1)
        self.certificate = Entry(master=secFrame, width=txtSize, font=small_font, bg=graybg)
        self.certificate.grid(row=1, column=2)

        # Certificate Password line
        paswImg = Label(master=secFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2, column=0)
        paswLabel = Label(master=secFrame, text='   Password:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg).grid(row=2, column=1)
        self.secPaswText = Entry(master=secFrame, width=txtSize, font=small_font, bg=whitebg, show=False)
        self.secPaswText.grid(row=2, column=2)

        secCanvas.grid(row=5, sticky='eswn')

        button = Button(self.login, text="Log In", highlightthickness=0, bg=buttonColor, fg=whitebg, activebackground=buttonColor,height=4, width=49, command=self.loginIn).grid(row=6)

    def close(self):
        self.login.destroy()
        reactor.callFromThread(reactor.stop)

    def start(self):
        self.login.wait_window()

    def loginIn(self):
        # create ACCOUNT and SAVE as default
        protocol = switch_protocol[self.comboProtocol.get()]
        name = self.nameText.get()
        password = self.paswText.get()
        clientID = self.idText.get()
        serverHost = self.hostText.get()
        serverPort = self.portText.get()
        cleanSession = self.varClean.get()
        keepAlive = self.keepText.get()
        will = self.willText.get()
        willT = self.willTText.get()
        qos = self.comboQos.get()
        enabled = self.varEnabled.get()
        certificate = self.certificate.get()
        self.certificate.text = ''
        certPasw = self.secPaswText.get()

        account = AccountEntity(protocol=protocol, username=name, password=password, clientID=clientID,
                                serverHost=serverHost,
                                port=serverPort, cleanSession=cleanSession, keepAlive=keepAlive, will=will,
                                willTopic=willT,
                                isRetain=True,
                                qos=qos, isDefault=False, isSecure=enabled, certificate=certificate, certPasw=certPasw)

        if AccountValidation.valid(account):
            datamanage = datamanager()

            previous = datamanage.get_account_clientID(account.clientID)
            if previous is None:
                    datamanage.add_entity(account)
                    account = datamanage.get_account_clientID(clientID)
                    datamanage.set_default_account_clientID(account.id)

                    self.login.destroy()
                    loading = Loading(self.root, self.app)
                    loading.start()
            else:
                messagebox.showinfo("Warning", "Wrong value for clientID='" + str(account.clientID) + "'. This one is already in use")
        else:
            if account.keepAlive is '' or (int(account.keepAlive) <= 0 or int(account.keepAlive)) > 65535:
                messagebox.showinfo("Warning", 'Wrong value for Keepalive')
            else:
                messagebox.showinfo("Warning", 'Please, fill in all required fileds: Username, Password, ClientID, Host, Port')

class NoteForm:

    def __init__(self, root, app, active, old):
        self.root = root
        self.app = app
        self.old = old
        self.active = active
        self.main = tk.Toplevel()
        center_child(self.main)
        self.main.geometry("350x570")

        self.note = ttk.Notebook(self.main, width=349, height=520)
        self.note.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        tab1 = Frame(self.note)
        tab2 = Frame(self.note)
        tab3 = Frame(self.note)
        tab4 = Frame(self.note)

        small_font = ('Verdana', 10)
        bold_font = ('Verdana', 9, 'bold')
        buttonColor = '#%02x%02x%02x' % (30, 144, 255)
        gui_style = ttk.Style()
        gui_style.configure('TNotebook', tabposition='s')
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
        gui_style.configure('My.TCombobox', background='white', border=0)

        delImage = Image.open('./resources/ic_delete_with_background.png')
        self.delPhoto = ImageTk.PhotoImage(delImage)

        #TOPICS FORM
        self.topicIDs = []

        topics = Label(tab1, text=" topics list:", font=bold_font).grid(row=0, sticky='w')
        # topics = Label(tab1, image=self.regPhoto).grid(row=0, sticky='w')

        topicsCanvas = tk.Canvas(tab1, width=359, height=350, bg='white', highlightcolor='white')
        topicsFrame = ttk.Frame(topicsCanvas, style='My.TFrame')

        datamanage = datamanager()
        account = datamanage.get_default_account()

        i = 0
        topics = None
        if account is not None:
            topics = datamanage.get_topics_all_accountID(account.id)

        qosImg = Image.open('./resources/icon_qos_0_75.png')
        self.photo0 = ImageTk.PhotoImage(qosImg)
        qosImg = Image.open('./resources/icon_qos_1_75.png')
        self.photo1 = ImageTk.PhotoImage(qosImg)
        qosImg = Image.open('./resources/icon_qos_2_75.png')
        self.photo2 = ImageTk.PhotoImage(qosImg)
        self.qosPhoto = self.photo0

        self.topicNames = []

        if topics is not None:
            if len(topics) > 0:
                for item in topics:
                    topicName = ' {}'.format(item.topicName)
                    self.topicNames.append(item.topicName)

                    if item.qos == 0:
                        self.qosPhoto = self.photo0
                    if item.qos == 1:
                        self.qosPhoto = self.photo1
                    if item.qos == 2:
                        self.qosPhoto = self.photo2

                    if (i % 2) == 0:
                        Label(master=topicsFrame, text=topicName, bd=0, height=2, width=36, bg='white', anchor="w").grid(row=i + 1, column=0, sticky='w')
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg='white').grid(row=i + 1, column=1, sticky='w')

                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel', command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2)
                    else:
                        Label(master=topicsFrame, text=topicName, bd=0, height=2, width=36, bg='gray92', anchor="w").grid(row=i + 1, column=0, sticky='w')
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg='gray92').grid(row=i + 1, column=1, sticky='w')

                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='gray92')
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel', command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2)
                    i += 1

        topicsCanvas.create_window(0, 0, anchor='nw', window=topicsFrame)
        # vbar = ttk.Scrollbar(topicsFrame, orient='vertical', command=canvas.yview)

        topicsCanvas.grid(row=1, column=0, sticky='eswn')
        # vbar.grid(row=1, column=2)

        newTopic = Label(tab1, text=" add new topic:", font=bold_font).grid(row=2, sticky='w')

        newCanvas = tk.Canvas(tab1, width=359, height=70, bg='white', highlightcolor='white')
        newFrame = ttk.Frame(newCanvas, style='My.TFrame')

        settingsImage = Image.open('./resources/settings34.png')
        self.settingsPhoto = ImageTk.PhotoImage(settingsImage)

        size = 34
        txtSize = 18

        # Topic Name line tab1
        nameImg = Label(master=newFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='gray92').grid(row=0, column=0)
        nameLabel = Label(master=newFrame, text='   Topic:', bd=0, height=2, width=25, anchor="w", bg='gray92').grid(row=0, column=1)
        self.nameText = Entry(master=newFrame, width=txtSize, font=small_font, bg='gray92')
        self.nameText.grid(row=0, column=2)

        # QoS line tab1
        qosImg = Label(master=newFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='white').grid(row=1, column=0)
        qosLabel = Label(master=newFrame, text='   QoS:', bd=0, height=2, width=25, anchor="w", bg='white').grid(row=1, column=1)
        self.comboQos = ttk.Combobox(master=newFrame, values=qos, width=10, style='My.TCombobox')
        self.comboQos.current(0)
        self.comboQos.grid(row=1, column=2, sticky='e')

        newCanvas.create_window(0, 0, anchor='nw', window=newFrame)
        newCanvas.grid(row=3, column=0, sticky='eswn')

        button = Button(tab1, text="Add", highlightthickness=0, bg=buttonColor, fg='white', activebackground=buttonColor,
                        height=4, width=49, command=self.createTopic, font=small_font).grid(row=4, sticky='w')
        # TOPICS FORM END
        # SEND FORM

        send = Label(tab2, text=" send new message:", font=bold_font).grid(row=0, sticky='w')
        # send = Label(tab2, image=self.regPhoto).grid(row=0, sticky='w')

        sendCanvas = tk.Canvas(tab2, width=359, height=440, bg='white', highlightcolor='white')
        sendFrame = ttk.Frame(sendCanvas, style='My.TFrame')

        # Content line tab2
        contentImg = Label(master=sendFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='white').grid(row=0, column=0)
        contentLabel = Label(master=sendFrame, text='   Content:', bd=0, height=3, width=25, anchor="w", bg='white').grid(row=0, column=1, sticky='w')
        self.contentText = Entry(master=sendFrame, width=txtSize, font=small_font, bg='white')
        self.contentText.grid(row=0, column=2, sticky='e')

        # Topic line tab2
        topicImg = Label(master=sendFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='gray92').grid(row=1, column=0)
        topicLabel = Label(master=sendFrame, text='   Topic:', bd=0, height=3, width=25, anchor="w",bg='gray92').grid(row=1, column=1)
        self.nameText2 = Entry(master=sendFrame, width=txtSize, font=small_font, bg='gray92')
        self.nameText2.grid(row=1, column=2)

        # QoS line tab1
        qosImg = Label(master=sendFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='white').grid(row=2,column=0)
        qosLabel = Label(master=sendFrame, text='   QoS:', bd=0, height=3, width=25, anchor="w", bg='white').grid(row=2, column=1)
        self.comboQos2 = ttk.Combobox(master=sendFrame, values=qos, width=10, style='My.TCombobox')
        self.comboQos2.current(0)
        self.comboQos2.grid(row=2, column=2, sticky='e')

        self.varRetain = BooleanVar()
        self.varDuplicate = BooleanVar()

        # Retain line
        retainImg = Label(master=sendFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='gray92').grid(row=3, column=0)
        retainLabel = Label(master=sendFrame, text='   Retain:', bd=0, height=3, width=25, anchor="w", bg='gray92').grid(row=3, column=1)
        self.retainCheck = Checkbutton(master=sendFrame, height=3, width=txtSize - 2, variable=self.varRetain, bd=0, anchor='e',bg='gray92', activebackground='gray92', highlightbackground='gray92',highlightthickness=0)
        self.retainCheck.grid(row=3, column=2)

        # Duplicate line
        dupImg = Label(master=sendFrame, image=self.settingsPhoto, bd=0, height=size, width=size, bg='white').grid(row=4, column=0)
        dupLabel = Label(master=sendFrame, text='   Duplicate:', bd=0, height=3, width=25, anchor="w", bg='white').grid(row=4, column=1)
        self.dupCheck = Checkbutton(master=sendFrame, height=2, width=txtSize - 2, variable=self.varDuplicate, bd=0, anchor='e', bg='white', activebackground='white', highlightbackground='white', highlightthickness=0)
        self.dupCheck.grid(row=4, column=2)

        sendCanvas.create_window(0, 0, anchor='nw', window=sendFrame)
        sendCanvas.grid(row=1, column=0, sticky='eswn')

        button = Button(tab2, text="Send", font=small_font, highlightthickness=0, bg=buttonColor, fg='white', activebackground=buttonColor, height=4, width=49, command=self.sendTopic).grid(row=2)
        # SEND FORM END
        # MESSAGES FORM

        messages = Label(tab3, text=" messages list:", font=bold_font).grid(row=0, sticky='w')
        # messages = Label(tab3, image=self.regPhoto).grid(row=0, sticky='w')
        messagesCanvas = tk.Canvas(tab3, width=359, height=510, bg='white', highlightcolor='white')
        messagesFrame = ttk.Frame(messagesCanvas, style='My.TFrame')

        datamanage = datamanager()
        account = datamanage.get_default_account()

        messages = None
        if account is not None:
            messages = datamanage.get_messages_all_accountID(account.id)

        qosImg = Image.open('./resources/icon_in_qos_0_75.png')
        self.photo0in = ImageTk.PhotoImage(qosImg)
        qosImg = Image.open('./resources/icon_in_qos_1_75.png')
        self.photo1in = ImageTk.PhotoImage(qosImg)
        qosImg = Image.open('./resources/icon_in_qos_2_75.png')
        self.photo2in = ImageTk.PhotoImage(qosImg)

        qosImg = Image.open('./resources/icon_out_qos_0_75.png')
        self.photo0out = ImageTk.PhotoImage(qosImg)
        qosImg = Image.open('./resources/icon_out_qos_1_75.png')
        self.photo1out = ImageTk.PhotoImage(qosImg)
        qosImg = Image.open('./resources/icon_out_qos_2_75.png')
        self.photo2out = ImageTk.PhotoImage(qosImg)

        i = 0
        if messages is not None:
            if len(messages) > 0:
                for item in messages:
                    text = ' ' + str(item.topicName) + '\n ' + str(item.content.decode('utf-8'))

                    if item.incoming:
                        if item.qos == 0:
                            self.photo = self.photo0in
                        if item.qos == 1:
                            self.photo = self.photo1in
                        if item.qos == 2:
                            self.photo = self.photo2in
                    else:
                        if item.qos == 0:
                            self.photo = self.photo0out
                        if item.qos == 1:
                            self.photo = self.photo1out
                        if item.qos == 2:
                            self.photo = self.photo2out

                    if (i % 2) == 0:
                        Label(master=messagesFrame, text=text, bd=0, height=3, width=38, anchor="w", bg='white', justify=LEFT, font =small_font).grid(row=0+i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg='white').grid(row=0+i, column=1)
                    else:
                        Label(master=messagesFrame, text=text, bd=0, height=3, width=38, anchor="w", bg='gray92', justify=LEFT, font =small_font).grid(row=0+i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg='white').grid(row=0+i, column=1)
                    i += 1

        messagesCanvas.create_window(0, 0, anchor='nw', window=messagesFrame)
        messagesCanvas.grid(row=1, column=0, sticky='eswn')

        # MESSAGES FORM END

        if self.active == 0:
            self.note.add(tab1, image=self.app.topicsImgBlue)
        else:
            self.note.add(tab1, image=self.app.topicsImg)

        if self.active == 1:
            self.note.add(tab2, image=self.app.sendImgBlue)
        else:
            self.note.add(tab2, image=self.app.sendImg)

        if self.active == 2:
            self.note.add(tab3, image=self.app.messImgBlue)
        else:
            self.note.add(tab3, image=self.app.messImg)

        self.note.add(tab4, image=self.app.outImg)
        self.note.select(self.active)
        self.note.grid(row=0, column=0)

    def delete(self, id):
        self.main.destroy()
        topicName = self.topicNames[id]
        # SEND UNSUBSCRIBE _________________________________________________________________________________SEND UNSUBSCRIBE
        self.app.client.unsubscribeFrom(topicName)

    def sendTopic(self):
        print('Send topic')
        datamanage = datamanager()
        content = str.encode(self.contentText.get())
        name = self.nameText2.get()
        qos = self.comboQos2.get()
        retain = self.varRetain.get()
        dup = self.varDuplicate.get()

        self.contentText.text = ''
        self.nameText2 = ''
        self.comboQos.current(0)

        self.main.destroy()
        # SEND PUBLISH _________________________________________________________________________________SEND PUBLISH
        contentDecoded = content.decode('utf8')
        self.app.client.publish(name, int(qos), contentDecoded, retain, dup)

        if int(qos) == 0:
            # ADD to DB
            datamanage = datamanager()
            account = datamanage.get_default_account()
            if account.protocol != 3:
                message = MessageEntity(content=content, qos=int(qos), topicName=name,
                                        incoming=False, isRetain=retain, isDub=dup, accountentity_id=account.id)
                datamanage.add_entity(message)
            note = NoteForm(self.root, self.app, 1, 1)
            note.start()


    def createTopic(self):
        print('Create topic')
        name = self.nameText.get()
        qos = self.comboQos.get()

        if name is not None and name != '':
            datamanage = datamanager()
            account = datamanage.get_default_account()
            previous = datamanage.get_topic_by_name_and_accountID(name, account.id)
            if isinstance(previous, TopicEntity):
                if previous.qos != int(qos):
                    datamanage.delete_topic_name(name)
                    previous = None

            if previous is None:
                index = self.isInList(name)

                if index is None:
                    # ADD to list
                    self.nameText.text = '';
                    self.comboQos.current(0);

                self.main.destroy()
                # SEND SUBSCRIBE _________________________________________________________________________________SEND SUBSCRIBE
                self.app.client.subscribeTo(name, int(qos))

            else:
                messagebox.showinfo("Warning","Wrong value for TopicName= '" + str(name) + "'. This one is already in use")
        else:
            messagebox.showinfo("Warning", "Please, fill in all required fields: TopicName")

    def isInList(self, name):
        for i in range(0, len(self.topicNames)):
            if self.topicNames[i] == name:
                return i
        return None

    def _on_tab_changed(self, event):
        event.widget.update_idletasks()
        tab = event.widget.nametowidget(event.widget.select())
        new = self.note.index(tab)

        if new == 0 and self.old != new:
            self.main.destroy()
            note = NoteForm(self.root, self.app, 0, 0)
            note.start()

        if new == 1 and self.old != new:
            self.main.destroy()
            note = NoteForm(self.root, self.app, 1, 1)
            note.start()

        if new == 2 and self.old != new:
            self.main.destroy()
            note = NoteForm(self.root, self.app, 2, 2)
            note.start()

        if new == 3:
            self.main.destroy()
            accounts = Accounts(self.root, self.app)
            accounts.start()
            # ______________________________________________________________________SEND___DISCONNECT
            if self.app.client is not None:
                self.app.client.disconnectWith(0)

    def start(self):
        self.main.wait_window()

class Main:
    def __init__(self):
        datamanage = datamanager()
        datamanage.create_db()
        datamanage.clearAccountsDefault()
        datamanage.clear_default_account()
        self.client = None

        self.mainWindow = tk.Tk()

        self.topicsImg = ImageTk.PhotoImage(Image.open("./resources/ic_topics_list_blue_75.png"))
        self.sendImg = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-1_75.png"))
        self.messImg = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-03_75.png"))
        self.outImg = ImageTk.PhotoImage(Image.open("./resources/logout75.png"))
        self.topicsImgBlue = ImageTk.PhotoImage(Image.open("./resources/ic_topics_list_blue-1_75.png"))
        self.sendImgBlue = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-2_75.png"))
        self.messImgBlue = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-03-1_75.png"))

        self.mainWindow.title("Iot Broker Client")
        self.mainWindow.geometry("1x1")
        center(self.mainWindow)

        loading = Loading(self.mainWindow, self)
        loading.start()
        #accounts = Accounts(self.mainWindow, self)
        #accounts.start()
        #login = Login(self.mainWindow, self)
        #login.start()
        #note = NoteForm(self.mainWindow, self, 0, 4)
        #note.start()

        #________CLOSE
        #self.mainWindow.destroy()
        #reactor.stop()


    def startDisplay(self) -> None:
        tksupport.install(self.mainWindow)
        # start the event loop
        reactor.run()

    def timeout(self):
        print('MAIN timeout______')

    def connackReceived(self, retCode):
        note = NoteForm(self.mainWindow, self, 0, 4)
        note.start()

    def pingrespReceived(self, coapFlag):
        pass

    def unsubackReceived(self, listTopics):
        datamanage = datamanager()
        for name in listTopics:
            datamanage.delete_topic_name(name)
        note = NoteForm(self.mainWindow, self, 0, 4)
        note.start()

    def subackReceived(self, topic, qos, returnCode):
        # store topic
        datamanage = datamanager()
        account = datamanage.get_default_account()
        if isinstance(topic, MQTopic):
            topicToDB = TopicEntity(topicName=topic.getName(), qos=qos.getValue(), accountentity_id=account.id)
            datamanage.add_entity(topicToDB)
        else:
            topicToDB = TopicEntity(topicName=topic, qos=qos.getValue(), accountentity_id=account.id)
            datamanage.add_entity(topicToDB)
        note = NoteForm(self.mainWindow, self, 0, 4)
        note.start()

    def pubackReceived(self, topic, qos, content, dup, retainFlag, returnCode):
        # print('App pubackReceived')
        # store Message
        datamanage = datamanager()
        account = datamanage.get_default_account()

        if isinstance(topic, FullTopic):
            topicName = topic.getValue()
        else:
            topicName = topic.getName()

        # print(' topicName=' + str(topicName))
        message = MessageEntity(content=bytes(content, encoding='utf_8'), qos=qos.getValue(), topicName=topicName,
                                incoming=False, isRetain=retainFlag, isDub=dup, accountentity_id=account.id)
        datamanage.add_entity(message)
        # print('App pubackReceived entity was saved')
        note = NoteForm(self.mainWindow, self, 1, 1)
        note.start()

    def disconnectReceived(self):
        messagebox.showinfo("Warning", 'Disconnect received from server')
        accounts = Accounts(self.mainWindow, self)
        accounts.start()

    def errorReceived(self, text):
        #print('MyApp errorReceived: ' + text)
        pass

protocols = ['mqtt', 'mqttsn', 'coap', 'websocket','amqp']
qos = ['0', '1', '2']

switch_protocol = {
            'mqtt': 1,
            'mqttsn': 2,
            'coap': 3,
            'websocket': 4,
            'amqp':5
        }

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    try:
        Main().startDisplay()
    except Exception as inst:
        print(type(inst))


