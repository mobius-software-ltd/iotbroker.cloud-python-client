try:
    import Tkinter as tk # this is for python2
    from Tkinter import *
    from Tkinter import ttk
    import Tkinter.messagebox as messagebox
    from PIL import ImageTk, Image
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

from twisted.internet import tksupport, reactor

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

class Main_screen(Frame):
    def __init__(self, master):
        master.title("Iot Broker Client")
        master.geometry("100x150")
        Frame.__init__(self, master)
        self.grid()
        root.withdraw()

        self.client = None

        datamanage = datamanager()
        datamanage.create_db()
        datamanage.clearAccountsDefault()
        datamanage.clear_default_account()

        self.topicsImg = ImageTk.PhotoImage(Image.open("./resources/ic_topics_list_blue_75.png"))
        self.sendImg = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-1_75.png"))
        self.messImg = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-03_75.png"))
        self.outImg = ImageTk.PhotoImage(Image.open("./resources/logout75.png"))
        self.topicsImgBlue = ImageTk.PhotoImage(Image.open("./resources/ic_topics_list_blue-1_75.png"))
        self.sendImgBlue = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-2_75.png"))
        self.messImgBlue = ImageTk.PhotoImage(Image.open("./resources/is_message_list_blue-03-1_75.png"))

        self.createLoading()

    def createLogin(self):
        self.login = Toplevel()
        self.app = Login(self.login, self)

    def createLoading(self):
        self.loading = Toplevel()
        self.app = Loading(self.loading, self)

    def createNote(self, active, old):
        self.note = Toplevel()
        self.app = NoteForm(self.note, self, active, old)

    def createAccounts(self):
        self.accounts = Toplevel()
        self.app = Accounts(self.accounts, self)

    def pingrespReceived(self, coapFlag):
        pass

    def connackReceived(self, retCode):
        self.loading.destroy()
        self.createNote(0, 4)

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
        self.note.destroy()
        self.createNote(0, 4)

    def unsubackReceived(self, listTopics):
        datamanage = datamanager()
        for name in listTopics:
            datamanage.delete_topic_name(name)
        self.note.destroy()
        self.createNote(0, 4)

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
        self.note.destroy()
        self.createNote(1, 1)

    def publishReceived(self, topic, qos, content, dup, retainFlag):
        #print('App publishReceived ' + str(content))
        # store Message
        datamanage = datamanager()
        account = datamanage.get_default_account()

        if isinstance(topic, FullTopic):
            topicName = topic.getValue()
        elif isinstance(topic, str):
            topicName = topic
        else:
            topicName = topic.getName()

        if isinstance(content, str):
            content = bytes(content, encoding='utf_8')

        message = MessageEntity(content=content, qos=qos.getValue(), topicName=topicName,
                                incoming=True, isRetain=retainFlag, isDub=dup, accountentity_id=account.id)
        datamanage.add_entity(message)
        self.note.destroy()
        self.createNote(1, 1)

    def disconnectReceived(self):
        messagebox.showinfo("Warning", 'Disconnect received from server')
        self.note.destroy()
        self.createAccounts()

    def errorReceived(self, text):
        #print('MyApp errorReceived: ' + text)
        pass

class Loading(Frame):
    def __init__(self, master, main):
        self.master = master
        self.master.geometry("200x150")
        self.master.title("Loading...")
        self.main = main
        Frame.__init__(self, self.master)
        center_child(self.master)
        self.grid()

        canvas = Canvas(self, bg='red', width=360, height=450)
        canvas.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        canvas.create_image(0, 0, anchor="nw", image=self.photoimage0)
        self.photoimage1 = ImageTk.PhotoImage(file="./resources/iotbroker_icon_big.png")
        canvas.create_image(180, 150, image=self.photoimage1)
        self.photoimage2 = ImageTk.PhotoImage(file="./resources/ic_loading_text.png")
        canvas.create_image(180, 320, image=self.photoimage2)

        self.progress = ttk.Progressbar(canvas, length=300, orient='horizontal', mode='determinate')
        canvas.create_window(30, 400, anchor=NW, window=self.progress, height=10)
        self.progress.start(30)
        self.after(3000, self.stop_progressbar)

    def stop_progressbar(self):
        self.progress.stop()
        self.progress.step(50)

        datamanage = datamanager()
        account = datamanage.get_default_account()

        if account is not None:
            print('connection to: ' + account.serverHost + ":" + str(account.port))
            if account.cleanSession:
                datamanage.clear_by_id(account.id)

            if account.protocol == 1:
                self.main.client = MQTTclient(account, self.main)
                self.main.client.goConnect()

            if account.protocol == 2:
                self.main.client = MQTTSNclient(account, self.main)
                self.main.client.goConnect()

            if account.protocol == 3:
                self.main.client = CoapClient(account, self.main)
                self.main.client.goConnect()

            if account.protocol == 4:
                self.main.client = WSclient(account, self.main)
                self.main.client.goConnect()
                time.sleep(1.5)

            if account.protocol == 5:
                self.main.client = AMQPclient(account, self.main)
                self.main.client.goConnect()
        else:
            self.master.destroy()
            self.main.accounts = Toplevel()
            self.main.app = Accounts(self.main.accounts, self.main)


    def show_main(self):
        self.master.destroy()
        root.deiconify()

class Accounts(Frame):
    def __init__(self, master, main):
        master.geometry("200x155")
        master.title("Accounts")
        self.main = main
        Frame.__init__(self, master)
        center_child(master)
        self.grid()

        master.protocol("WM_DELETE_WINDOW", self.close)
        accounts_font = font.Font(family='Sans', size=10, weight="normal")
        buttonColor = '#%02x%02x%02x' % (30, 144, 255)
        label = Label(self, text="Please select account", highlightthickness=0, bg=buttonColor, fg='white', height=3, width=53, font=font.Font(family='Sans', size=10, weight="normal")).grid(row=0)

        self.clientIDs = []
        gui_style = ttk.Style()

        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', background='white', border=0, height=3, width=46, font=accounts_font)

        canvas = tk.Canvas(self, width=360, height=370, bg='white', highlightcolor='white')

        myframe = ttk.Frame(canvas,  style='My.TFrame')

        buttonImage = Image.open('./resources/ic_delete_with_background.png')
        self.buttonPhoto = ImageTk.PhotoImage(buttonImage)

        datamanage = datamanager()
        accounts = datamanage.get_accounts_all()

        i = 0
        if len(accounts) > 0:
            for item in accounts:
                text = ' {}\n {}\n {}:{}'.format(switch_protocol_back[item.protocol].upper(), item.clientID, item.serverHost, item.port)
                self.clientIDs.append(item.clientID)
                txtButton = ttk.Button(myframe, text=text, style='My.TLabel', command=lambda x=i: self.connect(x)).grid(row=i+1)
                delButton = ttk.Button(myframe, image=self.buttonPhoto, text="Del", style='My.TLabel', command=lambda x=i: self.delete(x)).grid(row=i+1, column=1)
                i+=1

        canvas.create_window(0, 0, anchor='nw', window=myframe)
        vbar = ttk.Scrollbar(canvas, orient='vertical', command=canvas.yview)

        canvas.grid(row=1, column=0, sticky='eswn')
        if i > 10:
            vbar.place(x=352, y=1, height=370)
            vbar.set(1, 1)

        canvasButton = tk.Canvas(self, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.grid(row=2, column=0, sticky='eswn')
        button = Button(canvasButton, text="Add new account", activeforeground='white', font=font.Font(family='Sans', size=12, weight="bold"), highlightthickness=0, bg=buttonColor, fg='white', activebackground=buttonColor, height=2, width=35, command=self.createAccount).grid(row=2)

    def close(self):
        self.master.destroy()
        root.deiconify()
        reactor.callFromThread(reactor.stop)

    def createAccount(self):
        self.master.destroy()
        self.main.createLogin()

    def delete(self, id):
        clientID = self.clientIDs[id]
        datamanage = datamanager()
        account = datamanage.delete_account(clientID)
        self.master.destroy()
        self.main.createAccounts()

    def connect(self, id):
        clientID = self.clientIDs[id]
        datamanage = datamanager()
        datamanage.clear_default_account()
        datamanage.set_default_account_clientID(clientID)
        self.master.destroy()
        self.main.createLoading()

class Login(Frame):

    def __init__(self, master, main):
        master.geometry("200x355")
        master.title("Log In")
        self.main = main
        Frame.__init__(self, master)
        center_child(master)
        self.grid()

        #self.login.protocol("WM_DELETE_WINDOW", self.close)
        canvas = Canvas(self, bg='red', width=360, height=660, bd=0)
        canvas.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        canvas.create_image(0, 0, anchor="nw", image=self.photoimage0)

        buttonColor = '#%02x%02x%02x' % (30, 144, 255)
        small_font = font.Font(family='Sans', size=11, weight="normal")
        bold_font = font.Font(family='Sans', size=10, weight="bold")
        size = 32
        txtSize = 15

        self.varClean = BooleanVar()
        self.varEnabled = BooleanVar()

        gui_style = ttk.Style()
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=52)
        gui_style.configure('My.TCombobox', background=buttonColor, border=0, arrowcolor='white')

        settingsImage = Image.open('./resources/settings30.png')
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
        heightLabel = 2
        widthLabel = 20
        padY = 8
        padX = 5

        regInfo = Label(canvas, text=" registration info:", font=bold_font).place(x=5, y=5)
        regCanvas = tk.Canvas(canvas, width=359, height=225, bg=whitebg, highlightcolor=whitebg)
        regFrame = ttk.Frame(regCanvas, style='My.TFrame')
        regCanvas.create_window(0, 0, anchor='nw', window=regFrame)

        #Protocol line
        canvasProtocol = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasProtocol.grid(row=0, column=0, sticky='w')
        protocolImg = Label(master=canvasProtocol, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        protocolLabel = Label(master=canvasProtocol, text=' Protocol:', bd=0, height=heightLabel, width=widthLabel+5, anchor="w", bg=whitebg, font=small_font).grid(row=0, column=1, sticky='w')
        self.comboProtocol = ttk.Combobox(master=canvasProtocol, values=protocols, width=9, style='My.TCombobox', font=small_font)
        self.comboProtocol.current(0)
        self.comboProtocol.grid(row=0, column=2, sticky='e', pady=12)

        # Username line
        canvasUserName = Canvas(regFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasUserName.grid(row=1, column=0, sticky='w')
        userImg = Label(master=canvasUserName, image=self.userPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        userLabel = Label(master=canvasUserName, text=' Username:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg, font=small_font).grid(row=1, column=1, sticky='w')
        self.nameText = Entry(master=canvasUserName, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.nameText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Password line
        canvasPassword = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasPassword.grid(row=2, column=0, sticky='w')
        paswImg = Label(master=canvasPassword, image=self.paswPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2,column=0)
        paswLabel = Label(master=canvasPassword, text=' Password:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg, font=small_font).grid(row=2, column=1, sticky='w')
        self.paswText = Entry(master=canvasPassword, width=txtSize, font=small_font, bg=whitebg, show=False, bd=1)
        self.paswText.grid(row=2, column=2, sticky='w', pady=padY, padx=padX)

        # ClientID line
        canvasID = Canvas(regFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasID.grid(row=3, column=0, sticky='w')
        idImg = Label(master=canvasID, image=self.idPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=3,column=0)
        idLabel = Label(master=canvasID, text=' Client ID:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg, font=small_font).grid(row=3, column=1, sticky='w')
        self.idText = Entry(master=canvasID, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.idText.grid(row=3, column=2, sticky='w', pady=padY, padx=padX)

        # Host line
        canvasHost = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasHost.grid(row=4, column=0, sticky='w')
        hostImg = Label(master=canvasHost, image=self.hostPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=4, column=0)
        hostLabel = Label(master=canvasHost, text=' Server host:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg, font=small_font).grid(row=4, column=1, sticky='w')
        self.hostText = Entry(master=canvasHost, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.hostText.grid(row=4, column=2, sticky='w', pady=padY, padx=padX)

        # Port line
        canvasPort = Canvas(regFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasPort.grid(row=5, column=0, sticky='w')
        portImg = Label(master=canvasPort, image=self.hostPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=5,column=0)
        portLabel = Label(master=canvasPort, text=' Port:', bd=0, height=heightLabel, width=widthLabel, anchor="w",bg=graybg, font=small_font).grid(row=5, column=1, sticky='w')
        self.portText = Entry(master=canvasPort, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.portText.grid(row=5, column=2, sticky='w', pady=padY, padx=padX)

        regCanvas.place(x=0, y=25)

        settingsInfo = Label(canvas, text=" settings:", font=bold_font).place(x=5, y=255)
        setCanvas = tk.Canvas(canvas, width=359, height=210, bg=whitebg, highlightcolor=whitebg)
        setFrame = ttk.Frame(setCanvas, style='My.TFrame')
        setCanvas.create_window(0, 0, anchor='nw', window=setFrame)

        # Clean line
        canvasClean = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasClean.grid(row=0, column=0, sticky='w')
        portImg = Label(master=canvasClean, image=self.cleanPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0,column=0)
        portLabel = Label(master=canvasClean, text=' Clean session:', bd=0, height=heightLabel, width=widthLabel+4, anchor="w", bg=whitebg, font=small_font).grid(row=0, column=1)
        self.cleanCheck = Checkbutton(master=canvasClean, width=9, font=small_font, height=2, variable=self.varClean, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.cleanCheck.grid(row=0, column=2)

        # Keepalive line
        canvasAlive = Canvas(setFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasAlive.grid(row=1, column=0, sticky='w')
        keepImg = Label(master=canvasAlive, image=self.keepPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1,column=0)
        keepLabel = Label(master=canvasAlive, text=' Keepalive:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg, font=small_font).grid(row=1, column=1)
        self.keepText = Entry(master=canvasAlive, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.keepText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Will line
        canvasWill = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasWill.grid(row=2, column=0, sticky='w')
        willImg = Label(master=canvasWill, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2, column=0)
        willLabel = Label(master=canvasWill, text=' Will:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg, font=small_font).grid(row=2, column=1)
        self.willText = Entry(master=canvasWill, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.willText.grid(row=2, column=2, sticky='w', pady=padY, padx=padX)

        # Will topic line
        canvasWillT = Canvas(setFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasWillT.grid(row=3, column=0, sticky='w')
        keepImg = Label(master=canvasWillT, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=3,column=0)
        keepLabel = Label(master=canvasWillT, text=' Will topic:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg, font=small_font).grid(row=3, column=1)
        self.willTText = Entry(master=canvasWillT, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.willTText.grid(row=3, column=2, sticky='w', pady=padY, padx=padX)

        # Retain line
        canvasRet = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasRet.grid(row=4, column=0, sticky='w')
        retImg = Label(master=canvasRet, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=5,column=0)
        retLabel = Label(master=canvasRet, text=' Retain:', bd=0, height=heightLabel, width=widthLabel+4, anchor="w", bg=whitebg, font=small_font).grid(row=5, column=1)
        self.retainCheck = Checkbutton(master=canvasRet, width=9, font=small_font, height=2, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.retainCheck.grid(row=5, column=2)

        # QoS line
        canvasQos = Canvas(setFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasQos.grid(row=5, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=4, column=0)
        qosLabel = Label(master=canvasQos, text=' QoS:', bd=0, height=heightLabel, width=widthLabel+5, anchor="w", bg=graybg, font=small_font).grid(row=4, column=1)
        self.comboQos = ttk.Combobox(master=canvasQos, values=qos, width=9, style='My.TCombobox', font=small_font)
        self.comboQos.current(0)
        self.comboQos.grid(row=4, column=2, sticky='e', pady=12)

        setCanvas.place(x=0, y=275)

        security = Label(canvas, text=" security:", font=bold_font).place(x=0, y=490)
        secCanvas = tk.Canvas(canvas, width=359, height=105, bg=whitebg, highlightcolor=whitebg)
        secFrame = ttk.Frame(secCanvas, style='My.TFrame')
        secCanvas.create_window(0, 0, anchor='nw', window=secFrame)

        # Enable line
        canvasEnable = Canvas(secFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasEnable.grid(row=0, column=0, sticky='w')
        enableImg = Label(master=canvasEnable, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        enableLabel = Label(master=canvasEnable, text=' Enabled:', bd=0, height=heightLabel, width=widthLabel+4, anchor="w", bg=whitebg, font=small_font).grid(row=0, column=1)
        self.enabledCheck = Checkbutton(master=canvasEnable, width=9, font=small_font, height=2, variable=self.varEnabled, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.enabledCheck.grid(row=0, column=2)

        # Certificate line
        canvasCert = Canvas(secFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasCert.grid(row=1, column=0, sticky='w')
        certImg = Label(master=canvasCert, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        certLabel = Label(master=canvasCert, text=' Certificate:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=graybg, font=small_font).grid(row=1, column=1)

        self.certificate = Entry(master=canvasCert, text='test', width=txtSize, font=small_font, bg=graybg, bd=1)
        self.certificate.bind("<Button-1>", self.certificateInput)
        self.certificate.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Certificate Password line
        canvasPassw = Canvas(secFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasPassw.grid(row=2, column=0, sticky='w')
        paswImg = Label(master=canvasPassw, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2, column=0)
        paswLabel = Label(master=canvasPassw, text=' Password:', bd=0, height=heightLabel, width=widthLabel, anchor="w", bg=whitebg, font=small_font).grid(row=2, column=1)
        self.secPaswText = Entry(master=canvasPassw, width=txtSize, font=small_font, bg=whitebg, show=False, bd=1)
        self.secPaswText.grid(row=2, column=2, sticky='w', pady=padY, padx=padX)

        secCanvas.place(x=0, y=510)

        canvasButton = tk.Canvas(canvas, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.place(x=0, y=615)
        button = Button(canvasButton, text="Log In", activeforeground='white',
                        font=font.Font(family='Sans', size=12, weight="bold"), highlightthickness=0, bg=buttonColor,
                        fg='white', activebackground=buttonColor, height=2, width=35, command=self.loginIn).grid(row=2)

    def certificateInput(self, event):
        self.cert = Toplevel()
        self.app = Certificate(self.cert, self)

    def close(self):
        self.main.destroy()
        reactor.callFromThread(reactor.stop)

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

                    self.master.destroy()
                    self.main.createLoading()
            else:
                messagebox.showinfo("Warning", "Wrong value for clientID='" + str(account.clientID) + "'. This one is already in use")
        else:
            if account.keepAlive is '' or (int(account.keepAlive) <= 0 or int(account.keepAlive)) > 65535:
                messagebox.showinfo("Warning", 'Wrong value for Keepalive')
            else:
                messagebox.showinfo("Warning", 'Please, fill in all required fileds: Username, Password, ClientID, Host, Port')

class Certificate(Frame):

    def __init__(self, master, main):
        master.geometry("200x30")
        master.title("Certificate")
        self.main = main
        Frame.__init__(self, master)
        center_child(master)
        self.grid()

        self.canvas = Canvas(self, bg='red', width=360, height=300, bd=0)
        self.canvas.pack()

        self.TextArea = Text(self.canvas, width=49)
        ScrollBar = Scrollbar(self.canvas)
        ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=ScrollBar.set)
        ScrollBar.pack(side=RIGHT, fill=Y)
        self.TextArea.pack(expand=YES, fill=BOTH)

        canvasButton = tk.Canvas(self.master, width=52, height=4)
        canvasButton.place(x=140, y=270)
        button = Button(canvasButton, text="OK", font=font.Font(family='Sans', size=12, weight="bold"), height=1, width=5, command=self.close).pack(pady=20)#.grid(row=2)


    def close(self):
        text = self.TextArea.get(1.0, END)
        self.master.destroy()
        self.main.certificate.delete(0, END)
        self.main.certificate.insert(0, text)

class NoteForm(Frame):

    def __init__(self, master, main, active, old):

        master.geometry("190x270")
        #master.title("Loading...")
        self.main = main
        Frame.__init__(self, master)
        center_child(master)
        self.grid()

        self.old = old
        self.active = active
        #self.main.transient(root)

        self.note = ttk.Notebook(self, width=349, height=520)
        self.note.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        tab1 = Frame(self.note)
        tab2 = Frame(self.note)
        tab3 = Frame(self.note)
        tab4 = Frame(self.note)

        canvasTab1 = Canvas(tab1, bg='white', width=349, height=520, bd=0)
        canvasTab1.pack()
        canvasTab2 = Canvas(tab2, bg='white', width=349, height=520, bd=0)
        canvasTab2.pack()
        canvasTab3 = Canvas(tab3, bg='white', width=349, height=520, bd=0)
        canvasTab3.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        canvasTab1.create_image(0, 0, anchor="nw", image=self.photoimage0)
        canvasTab2.create_image(0, 0, anchor="nw", image=self.photoimage0)
        canvasTab3.create_image(0, 0, anchor="nw", image=self.photoimage0)

        small_font = ('Sans', 11)
        bold_font = ('Sans', 10, 'bold')
        buttonColor = '#%02x%02x%02x' % (30, 144, 255)
        gui_style = ttk.Style()
        gui_style.configure('TNotebook', tabposition='s')
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
        gui_style.configure('My.TCombobox', background=buttonColor, border=0, arrowcolor='white')

        delImage = Image.open('./resources/ic_delete_with_background.png')
        self.delPhoto = ImageTk.PhotoImage(delImage)

        # TOPICS FORM
        self.topicIDs = []

        topics = Label(canvasTab1, text=" topics list:", font=bold_font).grid(row=0, sticky='w', pady=5)
        topicsCanvas = tk.Canvas(canvasTab1, width=340, height=350, bg='white', highlightcolor='white')
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
                        Label(master=topicsFrame, text=topicName, bd=0, height=2, width=26, bg='white', anchor="w",
                              font=small_font).grid(row=i + 1, column=0, sticky='w')
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg='white').grid(row=i + 1, column=1,
                                                                                              sticky='w')

                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel',
                                   command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2, padx=5)
                    else:
                        Label(master=topicsFrame, text=topicName, bd=0, height=2, width=26, bg='gray92', anchor="w",
                              font=small_font).grid(row=i + 1, column=0, sticky='w')
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg='gray92').grid(row=i + 1, column=1,
                                                                                               sticky='w')

                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='gray92')
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel',
                                   command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2, padx=5)
                    i += 1

        vbarTopics = ttk.Scrollbar(tab1, orient='vertical', command=topicsCanvas.yview)
        if i > 11:
            vbarTopics.place(x=335, y=30, height=350)
            vbarTopics.set(1, 1)

        topicsCanvas.create_window(0, 0, anchor='nw', window=topicsFrame)
        topicsCanvas.grid(row=1, column=0, sticky='eswn')

        newTopic = Label(canvasTab1, text=" add new topic:", font=bold_font).grid(row=2, sticky='w', pady=5)

        newCanvas = tk.Canvas(canvasTab1, width=359, height=70, bg='white', highlightcolor='white')
        newFrame = ttk.Frame(newCanvas, style='My.TFrame')

        settingsImage = Image.open('./resources/settings30.png')
        self.settingsPhoto = ImageTk.PhotoImage(settingsImage)

        size = 30
        txtSize = 18
        padY = 8
        padX = 5

        # Topic Name line tab1
        canvasName = Canvas(newFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasName.grid(row=0, column=0, sticky='w')
        nameImg = Label(master=canvasName, image=self.settingsPhoto, bd=0, height=size, width=size,
                        bg='white').grid(row=0, column=0)
        nameLabel = Label(master=canvasName, text=' Topic:', bd=0, height=2, width=15, anchor="w", bg='white',
                          font=small_font).grid(row=0, column=1)
        self.nameText = Entry(master=canvasName, width=txtSize, font=small_font, bg='white', bd=1)
        self.nameText.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # QoS line tab1
        canvasQos = Canvas(newFrame, bg='gray92', width=360, height=40, highlightcolor='gray92', bd=0)
        canvasQos.grid(row=1, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg='gray92').grid(
            row=1, column=0)
        qosLabel = Label(master=canvasQos, text=' QoS:', bd=0, height=2, width=28, anchor="w", bg='gray92',
                         font=small_font).grid(row=1, column=1)
        self.comboQos = ttk.Combobox(master=canvasQos, values=qos, width=5, style='My.TCombobox', font=small_font)
        self.comboQos.current(0)
        self.comboQos.grid(row=1, column=2, sticky='e', pady=12)

        newCanvas.create_window(0, 0, anchor='nw', window=newFrame)
        newCanvas.grid(row=3, column=0, sticky='eswn')

        canvasButton = tk.Canvas(canvasTab1, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.grid(row=4, column=0, sticky='eswn')
        button = Button(canvasButton, text="Add", activeforeground='white',
                        font=font.Font(family='Sans', size=12, weight="bold"), highlightthickness=0, bg=buttonColor,
                        fg='white', activebackground=buttonColor, height=2, width=35,
                        command=self.createTopic).grid(row=0, sticky='w')
        # TOPICS FORM END

        # ____________________________________________________________________________________________________________________________________________________________________

        # SEND FORM

        send = Label(canvasTab2, text=" send message:", font=bold_font).grid(row=0, sticky='w', pady=5)

        sendCanvas = tk.Canvas(canvasTab2, width=359, height=450, bg='white', highlightcolor='white')
        sendFrame = ttk.Frame(sendCanvas, style='My.TFrame')

        # Content line tab2
        canvasContent = Canvas(sendFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasContent.grid(row=0, column=0, sticky='w')
        contentImg = Label(master=canvasContent, image=self.settingsPhoto, bd=0, height=size, width=size,
                           bg='white').grid(row=0)
        contentLabel = Label(master=canvasContent, text=' Content:', bd=0, height=2, width=15, anchor="w",
                             bg='white', font=small_font).grid(row=0, column=1, sticky='w')
        self.contentText = Entry(master=canvasContent, width=txtSize, font=small_font, bg='white', bd=1)
        self.contentText.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # Topic line tab2
        canvasTopic = Canvas(sendFrame, bg='gray92', width=360, height=40, highlightcolor='gray92', bd=0)
        canvasTopic.grid(row=1, column=0, sticky='w')
        topicImg = Label(master=canvasTopic, image=self.settingsPhoto, bd=0, height=size, width=size,
                         bg='gray92').grid(row=0)
        topicLabel = Label(master=canvasTopic, text=' Topic:', bd=0, height=2, width=15, anchor="w", bg='gray92',
                           font=small_font).grid(row=0, column=1, sticky='w')
        self.nameText2 = Entry(master=canvasTopic, width=txtSize, font=small_font, bg='gray92', bd=1)
        self.nameText2.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # QoS line tab1
        canvasQos = Canvas(sendFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasQos.grid(row=2, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg='white').grid(
            row=0)
        qosLabel = Label(master=canvasQos, text=' QoS:', bd=0, height=2, width=28, anchor="w", bg='white',
                         font=small_font).grid(row=0, column=1, sticky='w')
        self.comboQos2 = ttk.Combobox(master=canvasQos, values=qos, width=5, style='My.TCombobox', font=small_font)
        self.comboQos2.current(0)
        self.comboQos2.grid(row=0, column=2, sticky='e', pady=12)

        self.varRetain = BooleanVar()
        self.varDuplicate = BooleanVar()

        # Retain line
        canvasRet = Canvas(sendFrame, bg='gray92', width=360, height=40, highlightcolor='gray92', bd=0)
        canvasRet.grid(row=3, column=0, sticky='w')
        retainImg = Label(master=canvasRet, image=self.settingsPhoto, bd=0, height=size + 2, width=size,
                          bg='gray92').grid(row=0)
        retainLabel = Label(master=canvasRet, text=' Retain:', bd=0, height=2, width=23, anchor="w", bg='gray92',
                            font=small_font).grid(row=0, column=1, sticky='w')
        self.retainCheck = Checkbutton(master=canvasRet, height=2, width=9, font=small_font,
                                       variable=self.varRetain, bd=0, anchor='e', bg='gray92',
                                       activebackground='gray92', highlightbackground='gray92',
                                       highlightthickness=0)
        self.retainCheck.grid(row=0, column=2)

        # Duplicate line
        canvasDup = Canvas(sendFrame, bg='gray92', width=360, height=40, highlightcolor='gray92', bd=0)
        canvasDup.grid(row=4, column=0, sticky='w')
        dupImg = Label(master=canvasDup, image=self.settingsPhoto, bd=0, height=size + 2, width=size,
                       bg='white').grid(row=0)
        dupLabel = Label(master=canvasDup, text=' Duplicate:', bd=0, height=2, width=23, anchor="w", bg='white',
                         font=small_font).grid(row=0, column=1, sticky='w')
        self.dupCheck = Checkbutton(master=canvasDup, height=2, width=9, font=small_font,
                                    variable=self.varDuplicate, bd=0, anchor='e', bg='white',
                                    activebackground='white', highlightbackground='white', highlightthickness=0)
        self.dupCheck.grid(row=0, column=2)

        sendCanvas.create_window(0, 0, anchor='nw', window=sendFrame)
        sendCanvas.grid(row=1, column=0, sticky='eswn')

        canvasButton = tk.Canvas(canvasTab2, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.grid(row=2, column=0, sticky='eswn')
        button = Button(canvasButton, text="Send", activeforeground='white',
                        font=font.Font(family='Sans', size=12, weight="bold"), highlightthickness=0, bg=buttonColor,
                        fg='white', activebackground=buttonColor, height=2, width=35, command=self.sendTopic).grid(
            row=0, sticky='w')

        # SEND FORM END

        # ____________________________________________________________________________________________________________________________________________________________________

        # MESSAGES FORM

        messages = Label(canvasTab3, text=" messages list:", font=bold_font).grid(row=0, sticky='w', pady=5)
        messagesCanvas = tk.Canvas(canvasTab3, width=359, height=510, bg='white', highlightcolor='white')
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
                        Label(master=messagesFrame, text=text, bd=0, height=3, width=28, anchor="w", bg='white',
                              justify=LEFT, font=small_font).grid(row=i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg='white').grid(row=i, column=1)
                    else:
                        Label(master=messagesFrame, text=text, bd=0, height=3, width=28, anchor="w", bg='gray92',
                              justify=LEFT, font=small_font).grid(row=i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg='white').grid(row=i, column=1)
                    i += 1

        vbarMessages = ttk.Scrollbar(tab3, orient='vertical', command=messagesCanvas.yview)
        if i > 10:
            vbarMessages.place(x=335, y=30, height=490)
            vbarMessages.set(1, 1)

        messagesCanvas.create_window(0, 0, anchor='nw', window=messagesFrame)
        messagesCanvas.grid(row=1, column=0, sticky='eswn')

        # MESSAGES FORM END

        if self.active == 0:
            self.note.add(tab1, image=self.main.topicsImgBlue)
        else:
            self.note.add(tab1, image=self.main.topicsImg)

        if self.active == 1:
            self.note.add(tab2, image=self.main.sendImgBlue)
        else:
            self.note.add(tab2, image=self.main.sendImg)

        if self.active == 2:
            self.note.add(tab3, image=self.main.messImgBlue)
        else:
            self.note.add(tab3, image=self.main.messImg)

        self.note.add(tab4, image=self.main.outImg)
        self.note.select(self.active)
        self.note.grid(row=0, column=0)

    def delete(self, id):
        #self.main.destroy()
        topicName = self.topicNames[id]
        # SEND UNSUBSCRIBE _________________________________________________________________________________SEND UNSUBSCRIBE
        self.main.client.unsubscribeFrom(topicName)

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

        # SEND PUBLISH _________________________________________________________________________________SEND PUBLISH
        contentDecoded = content.decode('utf8')
        self.main.client.publish(name, int(qos), contentDecoded, retain, dup)

        if int(qos) == 0:
            # ADD to DB
            datamanage = datamanager()
            account = datamanage.get_default_account()
            if account.protocol != 3:
                message = MessageEntity(content=content, qos=int(qos), topicName=name,
                                        incoming=False, isRetain=retain, isDub=dup, accountentity_id=account.id)
                datamanage.add_entity(message)
            self.master.destroy()
            self.main.createNote(0, 4)

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

                # SEND SUBSCRIBE _________________________________________________________________________________SEND SUBSCRIBE
                self.main.client.subscribeTo(name, int(qos))

            else:
                messagebox.showinfo("Warning",
                                    "Wrong value for TopicName= '" + str(name) + "'. This one is already in use")
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
            self.master.destroy()
            self.main.createNote(0, 0)

        if new == 1 and self.old != new:
            self.master.destroy()
            self.main.createNote(1, 1)

        if new == 2 and self.old != new:
            self.master.destroy()
            self.main.createNote(2, 2)

        if new == 3:
            self.master.destroy()
            self.main.createAccounts()
            #_____________________________________________________________________SEND___DISCONNECT
            if self.main.client is not None:
                self.main.client.disconnectWith(0)

protocols = ['mqtt', 'mqttsn', 'coap', 'websocket','amqp']
qos = ['0', '1', '2']

switch_protocol = {
            'mqtt': 1,
            'mqttsn': 2,
            'coap': 3,
            'websocket': 4,
            'amqp':5
        }

switch_protocol_back = {
            1: 'mqtt',
            2: 'mqttsn',
            3: 'coap',
            4: 'websocket',
            5: 'amqp'
        }

root = Tk()
tksupport.install(root)
app = Main_screen(root)
reactor.run()