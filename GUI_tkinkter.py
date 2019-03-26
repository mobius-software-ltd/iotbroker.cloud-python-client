try:
    import Tkinter as tk # this is for python2
    from Tkinter import *
    from Tkinter import ttk
    import Tkinter.messagebox as messagebox
    from PIL import Image, ImageFont, ImageDraw, ImageTk
except:
    import tkinter as tk # this is for python3
    from tkinter import *
    from tkinter import ttk
    from tkinter import font
    import tkinter.messagebox as messagebox
    from PIL import Image, ImageFont, ImageDraw, ImageTk

from database import AccountEntity, TopicEntity, MessageEntity, Base, datamanager
from iot.classes.AccountValidation import *

from iot.mqtt.MQTTclient import *
from iot.mqttsn.MQTTSNclient import *
from iot.coap.CoapClient import *
from iot.websocket.WSclient import *
from iot.amqp.AMQPclient import *

from twisted.internet import tksupport, reactor

import textwrap

# for Custom Font Usage
font_bold="fonts/ClearSans-Bold.ttf"
font_regular="fonts/ClearSans-Regular.ttf"
font_medium="fonts/ClearSans-Medium.ttf"

# Custom Button Color
buttonColor = '#%02x%02x%02x' % (30, 144, 255)
whitebg = 'white'
graybg = 'gray92'

def truetype_font(font_path, size):
    return ImageFont.truetype(font_path, size)

class CustomFont_Label(Label):
    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, size=None, strings_number=1,
                 **kwargs):
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")

            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)

        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height*strings_number), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground, align='left')

        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)

class CustomFont_Button(Button):

    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, size=None, strings_number=1,
                 **kwargs):
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")

            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)

        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height*strings_number), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground, align='left')

        self._photoimage = ImageTk.PhotoImage(image)
        Button.__init__(self, master, image=self._photoimage, **kwargs)

def center_child(win, width, height):
    x = win.winfo_screenwidth() // 2 - width // 2
    y = win.winfo_screenheight() // 2 - height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class Main_screen(Frame):
    def __init__(self, master):
        master.title("Iot Broker Client")
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

    def createLogin(self, protocol):
        self.login = Toplevel()
        self.app = Login(self.login, self, protocol)

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
        if coapFlag:
            self.loading.destroy()
            self.createNote(0, 4)

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
        #print('App publishReceived content=' + str(content)+ 'topic=' + str(topic))
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
        #self.createAccounts()

    def errorReceived(self, text):
        #print('MyApp errorReceived: ' + text)
        pass

    def timeout(self):
        print('Timeout was reached. Try to reconnect')
        pass

class Loading(Frame):
    def __init__(self, master, main):
        self.master = master
        center_child(self.master, 360, 450)
        self.master.title("Loading...")
        self.main = main
        Frame.__init__(self, self.master)
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
        self.master = master
        center_child(self.master, 360, 455)
        master.title("iotbroker.cloud")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        master.protocol("WM_DELETE_WINDOW", self.close)

        label = CustomFont_Label(self, text="Please select account", foreground='white', font_path=font_bold, size=16, highlightthickness=0, bg=buttonColor, height=35, width=380).grid(row=0)

        self.clientIDs = []
        gui_style = ttk.Style()

        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', background='white', border=0, height=3, width=46)

        canvas = tk.Canvas(self, width=360, height=370, bg='white', highlightcolor='white', highlightthickness=0)

        myframe = ttk.Frame(canvas,  style='My.TFrame')

        buttonImage = Image.open('./resources/ic_delete_with_background.png')
        self.buttonPhoto = ImageTk.PhotoImage(buttonImage)

        datamanage = datamanager()
        accounts = datamanage.get_accounts_all()

        i = 0
        if len(accounts) > 0:
            for item in accounts:
                text = ' {} \n {} \n {}:{}'.format(switch_protocol_back[item.protocol].upper(), item.clientID, item.serverHost, item.port)
                num = 300 - len(item.serverHost)
                text += num * ' '
                self.clientIDs.append(item.clientID)
                txtButton = CustomFont_Button(myframe, text=text, font_path=font_medium, size=12, strings_number=4, background='white', highlightthickness=0, bd=0, height=50, width=300, command=lambda x=i: self.connect(x)).grid(row=i+1)
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
        button = CustomFont_Button(canvasButton, text="Add new account", foreground="white", font_path=font_bold, size=16, strings_number=1, bg=buttonColor, highlightthickness=0, bd=0, height=45, width=380, activeforeground='white', activebackground=buttonColor, command=self.createAccount).grid(row=2)

    def close(self):
        self.master.destroy()
        root.deiconify()
        reactor.callFromThread(reactor.stop)

    def createAccount(self):
        self.master.destroy()
        self.main.createLogin(1)

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

    def __init__(self, master, main, protocol):
        self.master = master
        center_child(self.master, 360, 660)
        master.title("Log In")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        #self.login.protocol("WM_DELETE_WINDOW", self.close)
        canvas = Canvas(self, bg='red', width=360, height=660, bd=0, highlightthickness=0)
        canvas.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        canvas.create_image(0, 0, anchor="nw", image=self.photoimage0)

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

        padY = 8
        padX = 5

        regInfo = CustomFont_Label(canvas, text=" registration info:", font_path=font_bold, size=14).place(x=5, y=2)
        regCanvas = tk.Canvas(canvas, width=359, height=225, bg=whitebg, highlightcolor=whitebg)
        regFrame = ttk.Frame(regCanvas, style='My.TFrame')
        regCanvas.create_window(0, 0, anchor='nw', window=regFrame)

        #Protocol line
        canvasProtocol = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasProtocol.grid(row=0, column=0, sticky='w')
        protocolImg = Label(master=canvasProtocol, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        text = ' Protocol:' + (200-len(' Protocol:'))*" "
        protocolLabel = CustomFont_Label(canvasProtocol, text=text, font_path=font_regular, size=16, bg=whitebg, width=220).grid(row=0, column=1, sticky='w')
        self.comboProtocol = ttk.Combobox(master=canvasProtocol, values=protocols, width=9, style='My.TCombobox', font=small_font)
        self.comboProtocol.current(protocol-1)
        self.comboProtocol.grid(row=0, column=2, sticky='e', pady=12)
        self.comboProtocol.bind('<<ComboboxSelected>>', self.protocolSelection)

        # Username line
        canvasUserName = Canvas(regFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        if protocol in[1,4,5]:
            canvasUserName.grid(row=1, column=0, sticky='w')
        userImg = Label(master=canvasUserName, image=self.userPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        text = ' Username:' + (100 - len(' Username:')) * " "
        userLabel = CustomFont_Label(canvasUserName, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=1, column=1, sticky='w')
        self.nameText = Entry(master=canvasUserName, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.nameText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Password line
        canvasPassword = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 4, 5]:
            canvasPassword.grid(row=2, column=0, sticky='w')
        paswImg = Label(master=canvasPassword, image=self.paswPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2,column=0)
        text = ' Password:' + (100 - len(' Password:')) * " "
        paswLabel = CustomFont_Label(canvasPassword, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=2, column=1, sticky='w')
        self.paswText = Entry(master=canvasPassword, show="*", width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.paswText.grid(row=2, column=2, sticky='w', pady=padY, padx=padX)

        # ClientID line
        canvasID = Canvas(regFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasID.grid(row=3, column=0, sticky='w')
        idImg = Label(master=canvasID, image=self.idPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=3,column=0)
        text = ' Client ID:' + (100 - len(' Client ID:')) * " "
        idLabel = CustomFont_Label(canvasID, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=3, column=1, sticky='w')
        self.idText = Entry(master=canvasID, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.idText.grid(row=3, column=2, sticky='w', pady=padY, padx=padX)

        # Host line
        canvasHost = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasHost.grid(row=4, column=0, sticky='w')
        hostImg = Label(master=canvasHost, image=self.hostPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=4, column=0)
        text = ' Server host:' + (100 - len(' Server host:')) * " "
        hostLabel = CustomFont_Label(canvasHost, text=text, font_path=font_regular, size=16, bg=whitebg,
                                     width=170).grid(row=4, column=1, sticky='w')
        self.hostText = Entry(master=canvasHost, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.hostText.grid(row=4, column=2, sticky='w', pady=padY, padx=padX)

        # Port line
        canvasPort = Canvas(regFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasPort.grid(row=5, column=0, sticky='w')
        portImg = Label(master=canvasPort, image=self.hostPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=5,column=0)
        text = ' Port:' + (100 - len(' Port:')) * " "
        portLabel = CustomFont_Label(canvasPort, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=5, column=1, sticky='w')
        self.portText = Entry(master=canvasPort, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.portText.grid(row=5, column=2, sticky='w', pady=padY, padx=padX)

        regCanvas.place(x=0, y=25)

        settingsInfo = CustomFont_Label(canvas, text=" settings:", font_path=font_bold, size=14).place(x=5, y=252)
        setCanvas = tk.Canvas(canvas, width=359, height=210, bg=whitebg, highlightcolor=whitebg)
        setFrame = ttk.Frame(setCanvas, style='My.TFrame')
        setCanvas.create_window(0, 0, anchor='nw', window=setFrame)

        # Clean line
        canvasClean = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 2, 4]:
            canvasClean.grid(row=0, column=0, sticky='w')
        cleanImg = Label(master=canvasClean, image=self.cleanPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0,column=0)
        text = ' Clean session:' + (100 - len(' Clean session:')) * " "
        cleanLabel = CustomFont_Label(canvasClean, text=text, font_path=font_regular, size=16, bg=whitebg, width=210, height=30).grid(row=0, column=1, sticky='w')
        self.cleanCheck = Checkbutton(master=canvasClean, width=9, font=small_font, height=2, variable=self.varClean, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.cleanCheck.grid(row=0, column=2)

        # Keepalive line
        canvasAlive = Canvas(setFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasAlive.grid(row=1, column=0, sticky='w')
        keepImg = Label(master=canvasAlive, image=self.keepPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1,column=0)
        text = ' Keepalive:' + (100 - len(' Keepalive:')) * " "
        keepLabel = CustomFont_Label(canvasAlive, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=1, column=1, sticky='w')
        self.keepText = Entry(master=canvasAlive, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.keepText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Will line
        canvasWill = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 2, 4]:
            canvasWill.grid(row=2, column=0, sticky='w')
        willImg = Label(master=canvasWill, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Will:' + (100 - len(' Will:')) * " "
        willLabel = CustomFont_Label(canvasWill, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.willText = Entry(master=canvasWill, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.willText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Will topic line
        canvasWillT = Canvas(setFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        if protocol in [1, 2, 4]:
            canvasWillT.grid(row=3, column=0, sticky='w')
        keepImg = Label(master=canvasWillT, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1,column=0)
        text = ' Will topic:' + (100 - len(' Will topic:')) * " "
        willTLabel = CustomFont_Label(canvasWillT, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=1, column=1, sticky='w')
        self.willTText = Entry(master=canvasWillT, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.willTText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Retain line
        canvasRet = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 2, 4]:
            canvasRet.grid(row=4, column=0, sticky='w')
        retImg = Label(master=canvasRet, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1,column=0)
        text = ' Retain:' + (100 - len(' Retain:')) * " "
        retLabel = CustomFont_Label(canvasRet, text=text, font_path=font_regular, size=16, bg=whitebg, width=210,height=30).grid(row=1, column=1, sticky='w')
        self.retainCheck = Checkbutton(master=canvasRet, width=9, font=small_font, height=2, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.retainCheck.grid(row=1, column=2)

        # QoS line
        canvasQos = Canvas(setFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        if protocol in [1, 2, 4]:
            canvasQos.grid(row=5, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        text = ' QoS:' + (100 - len(' QoS:')) * " "
        qosLabel = CustomFont_Label(canvasQos, text=text, font_path=font_regular, size=16, bg=graybg, width=220).grid(row=1, column=1, sticky='w')
        self.comboQos = ttk.Combobox(master=canvasQos, values=qos, width=9, style='My.TCombobox', font=small_font)
        self.comboQos.current(0)
        self.comboQos.grid(row=1, column=2, sticky='e', pady=12)

        setCanvas.place(x=0, y=275)

        security = CustomFont_Label(canvas, text=" security:", font_path=font_bold, size=14).place(x=5, y=487)
        secCanvas = tk.Canvas(canvas, width=359, height=105, bg=whitebg, highlightcolor=whitebg)
        secFrame = ttk.Frame(secCanvas, style='My.TFrame')
        secCanvas.create_window(0, 0, anchor='nw', window=secFrame)

        # Enable line
        canvasEnable = Canvas(secFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasEnable.grid(row=0, column=0, sticky='w')
        enableImg = Label(master=canvasEnable, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        text = ' Enabled:' + (100 - len('  Enabled:')) * " "
        enableLabel = CustomFont_Label(canvasEnable, text=text, font_path=font_regular, size=16, bg=whitebg, width=210, height=30).grid(row=0, column=1, sticky='w')
        self.enabledCheck = Checkbutton(master=canvasEnable, width=9, font=small_font, height=2, variable=self.varEnabled, bd=0, anchor='e', bg=whitebg, activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.enabledCheck.grid(row=0, column=2)

        # Certificate line
        canvasCert = Canvas(secFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasCert.grid(row=1, column=0, sticky='w')
        certImg = Label(master=canvasCert, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(row=1, column=0)
        text = ' Certificate:' + (100 - len(' Certificate:')) * " "
        certLabel = CustomFont_Label(canvasCert, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=1, column=1, sticky='w')
        self.certificate = Entry(master=canvasCert, text='test', width=txtSize, font=small_font, bg=graybg, bd=1)
        self.certificate.bind("<Button-1>", self.certificateInput)
        self.certificate.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Certificate Password line
        canvasPassw = Canvas(secFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasPassw.grid(row=2, column=0, sticky='w')
        paswImg = Label(master=canvasPassw, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Password:' + (100 - len(' Password:')) * " "
        paswLabel = CustomFont_Label(canvasPassw, text=text, font_path=font_regular, size=16, bg=graybg, width=170).grid(row=1, column=1, sticky='w')
        self.secPaswText = Entry(master=canvasPassw, width=txtSize, font=small_font, bg=whitebg, show="*", bd=1)
        self.secPaswText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        secCanvas.place(x=0, y=510)

        canvasButton = tk.Canvas(canvas, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.place(x=0, y=615)
        button = CustomFont_Button(canvasButton, text="Log In", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, bg=buttonColor, highlightthickness=0, bd=0, height=45,
                                   width=380, activeforeground='white', activebackground=buttonColor,
                                   command=self.loginIn).grid(row=2)

    def protocolSelection(self, event):
        protocol = switch_protocol[self.comboProtocol.get()]
        self.master.destroy()
        self.main.createLogin(protocol)

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
        self.master = master
        center_child(self.master, 360, 325)
        master.title("Certificate")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        self.canvas = Canvas(self, bg='red', width=360, height=300, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.TextArea = Text(self.canvas, width=49)
        ScrollBar = Scrollbar(self.canvas)
        ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=ScrollBar.set)
        ScrollBar.pack(side=RIGHT, fill=Y)
        self.TextArea.pack(expand=YES, fill=BOTH)

        canvasButton = tk.Canvas(self.master, width=52, height=4)
        canvasButton.place(x=140, y=270)
        button = Button(canvasButton, text="OK", font=font.Font(family='Sans', size=12, weight="bold"), height=1, width=5, command=self.close).pack(pady=20)


    def close(self):
        text = self.TextArea.get(1.0, END).rstrip()
        self.master.destroy()
        self.main.certificate.delete(0, END)
        self.main.certificate.insert(0, text)

class NoteForm(Frame):

    def __init__(self, master, main, active, old):
        self.master = master
        center_child(self.master, 355, 570)
        master.title("iotbroker.cloud")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        self.old = old
        self.active = active

        self.note = ttk.Notebook(self, width=349, height=520)
        self.note.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        tab1 = Frame(self.note)
        tab2 = Frame(self.note)
        tab3 = Frame(self.note)
        tab4 = Frame(self.note)

        canvasTab1 = Canvas(tab1, bg=whitebg, width=349, height=520, bd=0, highlightthickness=0)
        canvasTab1.pack()
        canvasTab2 = Canvas(tab2, bg=whitebg, width=349, height=520, bd=0, highlightthickness=0)
        canvasTab2.pack()
        canvasTab3 = Canvas(tab3, bg=whitebg, width=349, height=520, bd=0, highlightthickness=0)
        canvasTab3.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        canvasTab1.create_image(0, 0, anchor="nw", image=self.photoimage0)
        canvasTab2.create_image(0, 0, anchor="nw", image=self.photoimage0)
        canvasTab3.create_image(0, 0, anchor="nw", image=self.photoimage0)

        small_font = ('Sans', 11)
        bold_font = ('Sans', 10, 'bold')

        gui_style = ttk.Style()
        gui_style.configure('TNotebook', tabposition='s')
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
        gui_style.configure('My.TCombobox', background=buttonColor, border=0, arrowcolor='white')

        delImage = Image.open('./resources/ic_delete_with_background.png')
        self.delPhoto = ImageTk.PhotoImage(delImage)

        # TOPICS FORM
        self.topicIDs = []

        topics = CustomFont_Label(canvasTab1, text=" topics list:", font_path=font_bold, size=14).grid(row=0, sticky='w', pady=3)
        topicsCanvas = tk.Canvas(canvasTab1, width=340, height=350, bg=whitebg, highlightcolor=whitebg)
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

                    text = topicName + (200 - len(topicName)) * " "
                    if (i % 2) == 0:
                        CustomFont_Label(topicsFrame, text=text, font_path=font_medium, size=16, width=230, bg=whitebg).grid(row=i + 1, column=0, sticky='w')
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg=whitebg).grid(row=i + 1, column=1, sticky='w')
                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background=whitebg)
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel', command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2, padx=5)
                    else:
                        CustomFont_Label(topicsFrame, text=text, font_path=font_medium, size=16, width=230, bg=graybg).grid(row=i + 1,column=0)
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg=graybg).grid(row=i + 1, column=1, sticky='w')
                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background=graybg)
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel', command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2, padx=5)
                    i += 1

        vbarTopics = ttk.Scrollbar(tab1, orient='vertical', command=topicsCanvas.yview)
        if i > 11:
            vbarTopics.place(x=335, y=30, height=350)
            vbarTopics.set(1, 1)

        topicsCanvas.create_window(0, 0, anchor='nw', window=topicsFrame)
        topicsCanvas.grid(row=1, column=0, sticky='eswn')

        newTopic = CustomFont_Label(canvasTab1, text=" add new topic:", font_path=font_bold, size=14).grid(row=2, sticky='w', pady=3)
        newCanvas = tk.Canvas(canvasTab1, width=359, height=70, bg=whitebg, highlightcolor=whitebg)
        newFrame = ttk.Frame(newCanvas, style='My.TFrame')

        settingsImage = Image.open('./resources/settings30.png')
        self.settingsPhoto = ImageTk.PhotoImage(settingsImage)

        size = 30
        txtSize = 18
        padY = 8
        padX = 5

        # Topic Name line tab1
        canvasName = Canvas(newFrame, bg=whitebg, width=360, height=40, highlightcolor=whitebg, bd=0)
        canvasName.grid(row=0, column=0, sticky='w')
        nameImg = Label(master=canvasName, image=self.settingsPhoto, bd=0, height=size, width=size,
                        bg=whitebg).grid(row=0, column=0)

        text = ' Topic:' + (100 - len(' Topic:')) * " "
        nameLabel = CustomFont_Label(canvasName, text=text, font_path=font_regular, size=16, bg=whitebg, width=140).grid(row=0, column=1, sticky='w')
        self.nameText = Entry(master=canvasName, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.nameText.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # QoS line tab1
        canvasQos = Canvas(newFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasQos.grid(row=1, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=graybg).grid(
            row=1, column=0)
        text = ' QoS:' + (100 - len(' QoS:')) * " "
        qosLabel = CustomFont_Label(canvasQos, text=text, font_path=font_regular, size=16, bg=graybg, width=250).grid(row=1, column=1, sticky='w')
        self.comboQos = ttk.Combobox(master=canvasQos, values=qos, width=5, style='My.TCombobox', font=small_font)
        self.comboQos.current(0)
        self.comboQos.grid(row=1, column=2, sticky='e', pady=12)

        newCanvas.create_window(0, 0, anchor='nw', window=newFrame)
        newCanvas.grid(row=3, column=0, sticky='eswn')

        canvasButton = tk.Canvas(canvasTab1, width=52, height=4, bg='white', highlightcolor=whitebg)
        canvasButton.grid(row=4, column=0, sticky='eswn')

        button = CustomFont_Button(canvasButton, text="Add", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, bg=buttonColor, highlightthickness=0, bd=0, height=45,
                                   width=380, activeforeground=whitebg, activebackground=buttonColor,
                                   command=self.createTopic).grid(row=0, sticky='w')
        # TOPICS FORM END

        # ____________________________________________________________________________________________________________________________________________________________________

        # SEND FORM

        send = CustomFont_Label(canvasTab2, text=" send message:", font_path=font_bold, size=14).grid(row=0, sticky='w', pady=3)
        sendCanvas = tk.Canvas(canvasTab2, width=359, height=450, bg=whitebg, highlightcolor=whitebg)
        sendFrame = ttk.Frame(sendCanvas, style='My.TFrame')

        # Content line tab2
        canvasContent = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=whitebg, bd=0)
        canvasContent.grid(row=0, column=0, sticky='w')
        contentImg = Label(master=canvasContent, image=self.settingsPhoto, bd=0, height=size, width=size,
                           bg=whitebg).grid(row=0)

        text = ' Content:' + (100 - len(' Content:')) * " "
        contentLabel = CustomFont_Label(canvasContent, text=text, font_path=font_regular, size=16, bg=whitebg, width=140).grid(row=0, column=1, sticky='w')
        self.contentText = Entry(master=canvasContent, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.contentText.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # Topic line tab2
        canvasTopic = Canvas(sendFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasTopic.grid(row=1, column=0, sticky='w')
        topicImg = Label(master=canvasTopic, image=self.settingsPhoto, bd=0, height=size, width=size,
                         bg=graybg).grid(row=0)
        text = ' Topic:' + (100 - len(' Topic:')) * " "
        topicLabel = CustomFont_Label(canvasTopic, text=text, font_path=font_regular, size=16, bg=graybg,
                                        width=140).grid(row=0, column=1, sticky='w')
        self.nameText2 = Entry(master=canvasTopic, width=txtSize, font=small_font, bg=graybg, bd=1)
        self.nameText2.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # QoS line tab1
        canvasQos = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=whitebg, bd=0)
        canvasQos.grid(row=2, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(
            row=0)

        text = ' QoS:' + (100 - len(' QoS:')) * " "
        qosLabel = CustomFont_Label(canvasQos, text=text, font_path=font_regular, size=16, bg=whitebg, width=250).grid( row=0, column=1, sticky='w')
        self.comboQos2 = ttk.Combobox(master=canvasQos, values=qos, width=5, style='My.TCombobox', font=small_font)
        self.comboQos2.current(0)
        self.comboQos2.grid(row=0, column=2, sticky='e', pady=12)

        self.varRetain = BooleanVar()
        self.varDuplicate = BooleanVar()

        # Retain line
        canvasRet = Canvas(sendFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasRet.grid(row=3, column=0, sticky='w')
        retainImg = Label(master=canvasRet, image=self.settingsPhoto, bd=0, height=size + 2, width=size,
                          bg=graybg).grid(row=0)

        text = ' Retain:' + (100 - len(' Retain:')) * " "
        retainLabel = CustomFont_Label(canvasRet, text=text, font_path=font_regular, size=16, bg=graybg, width=210,
                                       height=30).grid(row=0, column=1, sticky='w')
        self.retainCheck = Checkbutton(master=canvasRet, height=2, width=9, font=small_font,
                                       variable=self.varRetain, bd=0, anchor='e', bg=graybg,
                                       activebackground=graybg, highlightbackground=graybg,
                                       highlightthickness=0)
        self.retainCheck.grid(row=0, column=2)

        # Duplicate line
        canvasDup = Canvas(sendFrame, bg=graybg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasDup.grid(row=4, column=0, sticky='w')
        dupImg = Label(master=canvasDup, image=self.settingsPhoto, bd=0, height=size + 2, width=size,
                       bg=whitebg).grid(row=0)
        text = ' Duplicate:' + (100 - len(' Duplicate:')) * " "
        dupLabel = CustomFont_Label(canvasDup, text=text, font_path=font_regular, size=16, bg=whitebg, width=210,
                                       height=30).grid(row=0, column=1, sticky='w')
        self.dupCheck = Checkbutton(master=canvasDup, height=2, width=9, font=small_font,
                                    variable=self.varDuplicate, bd=0, anchor='e', bg=whitebg,
                                    activebackground='white', highlightbackground=whitebg, highlightthickness=0)
        self.dupCheck.grid(row=0, column=2)

        sendCanvas.create_window(0, 0, anchor='nw', window=sendFrame)
        sendCanvas.grid(row=1, column=0, sticky='eswn')

        canvasButton = tk.Canvas(canvasTab2, width=52, height=4, bg=whitebg, highlightcolor=whitebg)
        canvasButton.grid(row=2, column=0, sticky='eswn')

        button = CustomFont_Button(canvasButton, text="Send", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, bg=buttonColor, highlightthickness=0, bd=0, height=45,
                                   width=380, activeforeground=whitebg, activebackground=buttonColor,
                                   command=self.sendTopic).grid(row=0, sticky='w')

        # SEND FORM END

        # ____________________________________________________________________________________________________________________________________________________________________

        # MESSAGES FORM

        messages = CustomFont_Label(canvasTab3, text=" messages list:", font_path=font_bold, size=14).grid(row=0, sticky='w', pady=3)
        #messages = Label(canvasTab3, text=" messages list:", font=bold_font).grid(row=0, sticky='w', pady=5)
        messagesCanvas = tk.Canvas(canvasTab3, width=359, height=510, bg=whitebg, highlightcolor=whitebg)
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
        scroll_flag = False
        if messages is not None:
            if len(messages) > 0:
                for item in messages:
                    content = str(item.content.decode('utf-8'))
                    if len(content) > 32:
                        text = ' ' + str(item.topicName) + '\n ' + self.format_context(content)
                    else:
                        text = ' ' + str(item.topicName) + '\n ' + content

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

                    text = text + (200 - len(text)) * " "
                    strings_number = len(content) // 32 + 2
                    if strings_number > 2:
                        strings_number += 7
                        scroll_flag = True
                    if (i % 2) == 0:
                        CustomFont_Label(messagesFrame, text=text, font_path=font_regular, size=16, strings_number=strings_number, width=250, height=20*strings_number, bg=whitebg).grid(row=i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg=whitebg).grid(row=i, column=1)
                    else:
                        CustomFont_Label(messagesFrame, text=text, font_path=font_regular, size=16, strings_number=strings_number, width=250, height=20*strings_number, bg=graybg).grid(row=i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg=whitebg).grid(row=i, column=1)
                    i += 1

        vbarMessages = ttk.Scrollbar(tab3, orient='vertical', command=messagesCanvas.yview)
        if i > 10 or scroll_flag:
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

    def format_context(self, text):
        data = textwrap.wrap(text, 32)
        result = ''
        for piece in data:
            result += piece+'\n'
        return result

    def delete(self, id):
        #self.main.destroy()
        topicName = self.topicNames[id]
        # SEND UNSUBSCRIBE _________________________________________________________________________________SEND UNSUBSCRIBE
        self.main.client.unsubscribeFrom(topicName)

    def sendTopic(self):
        #print('Send topic')
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
        #print('Create topic')
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
