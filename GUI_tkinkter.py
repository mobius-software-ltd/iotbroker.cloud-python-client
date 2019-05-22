try:
    import Tkinter as tk  # this is for python2
    from Tkinter import *
    from Tkinter import ttk
    import Tkinter.messagebox as messagebox
    from PIL import Image, ImageFont, ImageDraw, ImageTk
except:
    import tkinter as tk  # this is for python3
    from tkinter import *
    from tkinter import ttk
    from tkinter import font
    import tkinter.messagebox as messagebox
    from PIL import Image, ImageFont, ImageDraw, ImageTk

from database import AccountEntity, MessageEntity, datamanager
from iot.classes.AccountValidation import *
from iot.mqtt.MQTTclient import *
from iot.mqttsn.MQTTSNclient import *
from iot.coap.CoapClient import *
from iot.websocket.WSclient import *
from iot.amqp.AMQPclient import *
from twisted.internet import tksupport, reactor

import textwrap
import sys
import logging
import protocol as client_protocol
import iot.network.certificate_validator as certificate_validator
import time

# for Custom Font Usage
font_bold = "fonts/ClearSans-Bold.ttf"
font_regular = "fonts/ClearSans-Regular.ttf"
font_medium = "fonts/ClearSans-Medium.ttf"

# Custom Button Color
buttonColor = '#%02x%02x%02x' % (30, 144, 255)
whitebg = 'white'
graybg = 'gray86'


def truetype_font(font_path, size):
    return ImageFont.truetype(font_path, size)


class CustomFont_Label(Label):
    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, size=None, strings_number=1, **kwargs):
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")

            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)

        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height * strings_number), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground)

        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)


class CustomFont_Button(Button):

    def __init__(self, master, text, foreground="black", truetype_font=None, font_path=None, size=None, strings_number=1, long=1, offset_x=0, offset_y=0, **kwargs):
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")

            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)

        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width * long, height * strings_number), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.text((offset_x, offset_y), text, font=truetype_font, fill=foreground)

        self._photoimage = ImageTk.PhotoImage(image)
        Button.__init__(self, master, image=self._photoimage, anchor='center', **kwargs)


def center_child(win, width, height):
    x = win.winfo_screenwidth() // 2 - width // 2
    y = win.winfo_screenheight() // 2 - height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def logo_panel(toplevel):
    if (sys.platform.startswith('win')):
        toplevel.iconbitmap('./resources/iotbroker_icon_big.ico')
    else:
        logo = PhotoImage(file='./resources/iotbroker_icon_big.gif')
        toplevel.tk.call('wm', 'iconphoto', toplevel._w, logo)


class Main_screen(Frame):
    def __init__(self, master):
        master.title("Iot Broker Client")
        Frame.__init__(self, master)
        self.grid()
        root.withdraw()

        self.client = None
        self.master = master

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

        self.show_loading(500)

    def show_loading(self, loading_timeout):
        if not hasattr(self, "loading") or self.loading is None:
            self.loading = tk.Toplevel(root)
            self.loading.group(root)
            self.loading_frame = Loading(self.loading, self)
            self.app = self.loading_frame
        else:
            self.loading.deiconify()
        self.loading_frame.do_load(loading_timeout)

    def show_login(self, protocol):
        if not hasattr(self, "login") or self.login is None:
            self.login = tk.Toplevel(root)
            self.login.group(root)
            self.login_frame = Login(self.login, self, protocol)
            self.app = self.login_frame
        else:
            self.login.deiconify()
        self.login_frame.login_refresh(protocol)

    def show_accounts(self):
        if not hasattr(self, "accounts") or self.accounts is None:
            self.accounts = tk.Toplevel(root)
            self.accounts.group(root)
            self.accounts_frame = Accounts(self.accounts, self)
            self.app = self.accounts_frame
        else:
            self.accounts.deiconify()

        self.accounts_frame.refresh_frame()
        self.accounts_frame.fill_accounts()

    def show_note(self, active, old):
        if not hasattr(self, "note") or self.note is None:
            self.note = tk.Toplevel(root)
            self.note.group(root)
            self.note_frame = NoteForm(self.note, self, active, old)
            self.app = self.note_frame
        else:
            self.note.deiconify()
            self.note_frame.change_active_tab(0)
            self.note_frame.refresh_all()

    def pingrespReceived(self, coapFlag):
        if coapFlag:
            self.loading.withdraw()
            self.show_note(0, 4)

    def connackReceived(self, retCode):
        self.loading.withdraw()
        self.show_note(0, 4)

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

        self.note_frame.refresh_topics()

    def unsubackReceived(self, listTopics):
        datamanage = datamanager()
        for name in listTopics:
            datamanage.delete_topic_name(name)
        self.note_frame.refresh_topics()

    def pubackReceived(self, topic, qos, content, dup, retainFlag, returnCode=None):
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

        message = MessageEntity(content=content, qos=qos.getValue(), topicName=topicName, incoming=False, isRetain=retainFlag, isDub=dup, accountentity_id=account.id)
        datamanage.add_entity(message)
        self.note_frame.refresh_messages()

    def publishReceived(self, topic, qos, content, dup, retainFlag):
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

        message = MessageEntity(content=content, qos=qos.getValue(), topicName=topicName, incoming=True, isRetain=retainFlag, isDub=dup, accountentity_id=account.id)
        datamanage.add_entity(message)
        self.note_frame.refresh_messages()

    def disconnectReceived(self):
        self.loading.withdraw()

    def errorReceived(self):
        self.disconnectReceived()
        self.show_accounts()

    def timeout(self):
        self.disconnectReceived()
        self.show_accounts()

    def show_error_message(self, title, message):
        messagebox.showinfo(title, message)

class Loading(Frame):
    def __init__(self, master, main):
        self.master = master
        self.master.resizable(False, False)
        self.master.title("Loading...")
        self.main = main
        Frame.__init__(self, self.master)
        self.grid()

        logo_panel(self.main.loading)

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

    def do_load(self, loading_timeout):
        center_child(self.master, 360, 450)
        self.progress.start(int(loading_timeout / 500))
        self.after(loading_timeout, self.stop_progressbar)

    def stop_progressbar(self):
        self.progress.stop()
        account = datamanager().get_default_account()

        if account is not None:
            print('connection to: ' + account.serverHost + ":" + str(account.port))
            try:
                if account.cleanSession:
                    datamanager().clear_by_id(account.id)

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

                if account.protocol == 5:
                    topics = datamanager().get_topics_all_accountID(account.id)
                    self.main.client = AMQPclient(account, self.main, topics)
                    self.main.client.goConnect()
            except Exception as err:
                datamanager().clear_default_account()
                messagebox.showinfo("Connect Error", str(err))
                self.main.errorReceived()
        else:
            self.main.loading.withdraw()
            self.main.show_accounts()


class Accounts(Frame):

    def __init__(self, master, main):
        self.master = master
        self.master.resizable(False, False)
        master.title("iotbroker.cloud")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        logo_panel(self.main.accounts)

        master.protocol("WM_DELETE_WINDOW", self.close)

        label = CustomFont_Label(self, text="Please select account", foreground='white', font_path=font_bold, size=16, highlightthickness=0, bg=buttonColor, height=35, width=380).grid(row=0)

        gui_style = ttk.Style()

        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', background='white', border=0, height=3, width=46)

        self.canvas = tk.Canvas(self, width=360, height=370, bg='white', highlightcolor='white', highlightthickness=0)
        self.vbar = ttk.Scrollbar(self.canvas, orient='vertical')
        self.myframe = ttk.Frame(self.canvas, style='My.TFrame')

        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.grid(row=1, column=0, sticky='eswn')

        buttonImage = Image.open('./resources/ic_delete_with_background.png')
        self.buttonPhoto = ImageTk.PhotoImage(buttonImage)

        canvasButton = tk.Canvas(self, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.grid(row=2, column=0, sticky='eswn')
        button = CustomFont_Button(canvasButton, text="Add new account", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, bg=buttonColor, highlightthickness=0, bd=0, height=45,
                                   width=380, activeforeground='white', activebackground=buttonColor,
                                   command=self.createAccount).grid(row=2)

        userImage = Image.open('./resources/username.png')
        self.userPhoto = ImageTk.PhotoImage(userImage)

    def refresh_frame(self):
        self.bind("<Destroy>", self._destroy)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        center_child(self.master, 360, 455)

    def fill_accounts(self):

        for widget in self.myframe.winfo_children():
            widget.destroy()

        accounts = datamanager().get_accounts_all()

        width = 260
        height = 370
        i = 0
        if len(accounts) > 0:

            if len(accounts) > 7:
                height = 53 * len(accounts)

            for item in accounts:

                userImg = Label(master=self.myframe, image=self.userPhoto, bd=0, height=50, width=50, bg=whitebg).grid(row=i + 1, column=0)

                text = ' {} \n {} \n {}:{}'.format(client_protocol.get_protocol_name(item.protocol).upper(), item.clientID,
                                                   item.serverHost, item.port)
                num = 300 - len(item.serverHost)
                text += num * ' '
                txtButton = CustomFont_Button(self.myframe, text=text, font_path=font_medium, size=12, strings_number=4,
                                              background='white', highlightthickness=0, bd=0, height=50, width=width,
                                              command=lambda curr_client_id=item.clientID: self.connect(curr_client_id)).grid(row=i + 1, column=1)
                delButton = ttk.Button(self.myframe, image=self.buttonPhoto, text="Del", style='My.TLabel', command=lambda curr_client_id=item.clientID: self.delete(curr_client_id)).grid(row=i + 1, column=2)
                i += 1

        self.vbar.place(x=342, y=1, height=370)
        self.vbar.set(1, 1)
        self.canvas.configure(scrollregion=(0, 0, 359, height))

        self.canvas.create_window(0, 0, anchor='nw', window=self.myframe)

    def _on_mousewheel(self, event):
        scroll = 1 if event.num == 5 else -1
        self.canvas.yview_scroll(scroll, "units")

    def close(self):
        self.master.destroy()
        root.deiconify()
        reactor.callFromThread(reactor.stop)

    def _destroy(self, event):
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def createAccount(self):
        self.main.accounts.withdraw()
        self.main.show_login(1)

    def delete(self, clientID):
        delete_account = datamanager().get_account_clientID(clientID)
        if delete_account is not None:
            datamanager().delete_account(delete_account.id)
            self.fill_accounts()

    def connect(self, clientID):
        print("connecting " + clientID)
        datamanage = datamanager()
        datamanage.clear_default_account()
        datamanage.set_default_account_clientID(clientID)
        self.main.accounts.withdraw()
        self.main.show_loading(1000)


class Login(Frame):

    def __init__(self, master, main, protocol):
        self.master = master
        self.master.resizable(False, False)
        master.title("Log In")
        self.main = main
        Frame.__init__(self, master)
        self.pack()
        self.protocol = protocol
        logo_panel(self.main.login)

        self.main.login.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self, bg='white', width=360, height=660, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        self.canvas.create_image(0, 0, anchor="nw", image=self.photoimage0)

    def login_refresh(self, protocol):
        center_child(self.master, 360, 660)
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

        padY = 4
        padX = 5

        regInfo = CustomFont_Label(self.canvas, text=" registration info:", font_path=font_bold, size=14).place(x=5, y=2)
        regCanvas = tk.Canvas(self.canvas, width=359, height=225, bg=whitebg, highlightcolor=whitebg)
        regFrame = ttk.Frame(regCanvas, style='My.TFrame')
        regCanvas.create_window(0, 0, anchor='nw', window=regFrame)

        # Protocol line
        canvasProtocol = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasProtocol.grid(row=0, column=0, sticky='w')
        protocolImg = Label(master=canvasProtocol, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        text = ' Protocol:' + (200 - len(' Protocol:')) * " "
        protocolLabel = CustomFont_Label(canvasProtocol, text=text, font_path=font_regular, size=16, bg=whitebg, width=220).grid(row=0, column=1, sticky='w')
        self.comboProtocol = ttk.Combobox(master=canvasProtocol, values=client_protocol.protocol_names(), width=9, style='My.TCombobox', font=small_font)
        self.comboProtocol.current(protocol - 1)
        self.comboProtocol.grid(row=0, column=2, sticky='e', pady=12)
        self.comboProtocol.bind('<<ComboboxSelected>>', self.protocolSelection)

        # Username line
        canvasUserName = Canvas(regFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        if protocol in [1, 4, 5]:
            canvasUserName.grid(row=1, column=0, sticky='w')
        userImg = Label(master=canvasUserName, image=self.userPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Username:' + (100 - len(' Username:')) * " "
        userLabel = CustomFont_Label(canvasUserName, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.nameText = Entry(master=canvasUserName, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.nameText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Password line
        canvasPassword = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 4, 5]:
            canvasPassword.grid(row=2, column=0, sticky='w')
        paswImg = Label(master=canvasPassword, image=self.paswPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=2, column=0)
        text = ' Password:' + (100 - len(' Password:')) * " "
        paswLabel = CustomFont_Label(canvasPassword, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=2, column=1, sticky='w')
        self.paswText = Entry(master=canvasPassword, show="*", width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.paswText.grid(row=2, column=2, sticky='w', pady=padY, padx=padX)

        # ClientID line
        canvasID = Canvas(regFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasID.grid(row=3, column=0, sticky='w')
        idImg = Label(master=canvasID, image=self.idPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=3, column=0)
        text = ' Client ID:' + (100 - len(' Client ID:')) * " "
        idLabel = CustomFont_Label(canvasID, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=3, column=1, sticky='w')
        self.idText = Entry(master=canvasID, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.idText.grid(row=3, column=2, sticky='w', pady=padY, padx=padX)

        # Host line
        canvasHost = Canvas(regFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasHost.grid(row=4, column=0, sticky='w')
        hostImg = Label(master=canvasHost, image=self.hostPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=4, column=0)
        text = ' Server host:' + (100 - len(' Server host:')) * " "
        hostLabel = CustomFont_Label(canvasHost, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=4, column=1, sticky='w')
        self.hostText = Entry(master=canvasHost, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.hostText.grid(row=4, column=2, sticky='w', pady=padY, padx=padX)

        # Port line
        canvasPort = Canvas(regFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasPort.grid(row=5, column=0, sticky='w')
        portImg = Label(master=canvasPort, image=self.hostPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=5, column=0)
        text = ' Port:' + (100 - len(' Port:')) * " "
        portLabel = CustomFont_Label(canvasPort, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=5, column=1, sticky='w')
        self.portText = Entry(master=canvasPort, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.portText.grid(row=5, column=2, sticky='w', pady=padY, padx=padX)

        regCanvas.place(x=0, y=25)

        settingsInfo = CustomFont_Label(self.canvas, text=" settings:", font_path=font_bold, size=14).place(x=5, y=252)
        setCanvas = tk.Canvas(self.canvas, width=359, height=210, bg=whitebg, highlightcolor=whitebg)
        setFrame = ttk.Frame(setCanvas, style='My.TFrame')
        setCanvas.create_window(0, 0, anchor='nw', window=setFrame)

        # Clean line
        canvasClean = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 2, 4]:
            canvasClean.grid(row=0, column=0, sticky='w')
        cleanImg = Label(master=canvasClean, image=self.cleanPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        text = ' Clean session:' + (100 - len(' Clean session:')) * " "
        cleanLabel = CustomFont_Label(canvasClean, text=text, font_path=font_regular, size=16, bg=whitebg, width=210, height=30).grid(row=0, column=1, sticky='w')
        self.cleanCheck = Checkbutton(master=canvasClean, width=9, font=small_font, height=2, variable=self.varClean, bd=0, anchor='e', bg=whitebg, activebackground=whitebg,
                                      highlightbackground=whitebg, highlightthickness=0)
        self.cleanCheck.grid(row=0, column=2)

        # Keepalive line
        canvasAlive = Canvas(setFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasAlive.grid(row=1, column=0, sticky='w')
        keepImg = Label(master=canvasAlive, image=self.keepPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Keepalive:' + (100 - len(' Keepalive:')) * " "
        keepLabel = CustomFont_Label(canvasAlive, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.keepText = Entry(master=canvasAlive, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.keepText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Will line
        canvasWill = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 2, 4]:
            canvasWill.grid(row=2, column=0, sticky='w')
        willImg = Label(master=canvasWill, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Will:' + (100 - len(' Will:')) * " "
        willLabel = CustomFont_Label(canvasWill, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.willText = Entry(master=canvasWill, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.willText.bind("<Button-1>", self.willInput)
        self.willText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Will topic line
        canvasWillT = Canvas(setFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        if protocol in [1, 2, 4]:
            canvasWillT.grid(row=3, column=0, sticky='w')
        keepImg = Label(master=canvasWillT, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Will topic:' + (100 - len(' Will topic:')) * " "
        willTLabel = CustomFont_Label(canvasWillT, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.willT = Entry(master=canvasWillT, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.willT.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Retain line
        canvasRet = Canvas(setFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        if protocol in [1, 2, 4]:
            canvasRet.grid(row=4, column=0, sticky='w')
        retImg = Label(master=canvasRet, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Retain:' + (100 - len(' Retain:')) * " "
        retLabel = CustomFont_Label(canvasRet, text=text, font_path=font_regular, size=16, bg=whitebg, width=210, height=30).grid(row=1, column=1, sticky='w')
        self.retainCheck = Checkbutton(master=canvasRet, width=9, font=small_font, height=2, bd=0, anchor='e',
                                       bg=whitebg, activebackground=whitebg, highlightbackground=whitebg,
                                       highlightthickness=0)
        self.retainCheck.grid(row=1, column=2)

        # QoS line
        canvasQos = Canvas(setFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        if protocol in [1, 2, 4]:
            canvasQos.grid(row=5, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' QoS:' + (100 - len(' QoS:')) * " "
        qosLabel = CustomFont_Label(canvasQos, text=text, font_path=font_regular, size=16, bg=whitebg, width=220).grid(row=1, column=1, sticky='w')
        self.comboQos = ttk.Combobox(master=canvasQos, values=client_protocol.qos_list(self.protocol), width=9, style='My.TCombobox', font=small_font)
        self.comboQos.current(0)
        self.comboQos.grid(row=1, column=2, sticky='e', pady=12)

        setCanvas.place(x=0, y=275)

        security = CustomFont_Label(self.canvas, text=" security:", font_path=font_bold, size=14).place(x=5, y=487)
        secCanvas = tk.Canvas(self.canvas, width=359, height=105, bg=whitebg, highlightcolor=whitebg)
        secFrame = ttk.Frame(secCanvas, style='My.TFrame')
        secCanvas.create_window(0, 0, anchor='nw', window=secFrame)

        # Enable line
        canvasEnable = Canvas(secFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasEnable.grid(row=0, column=0, sticky='w')
        enableImg = Label(master=canvasEnable, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)
        text = ' Enabled:' + (100 - len('  Enabled:')) * " "
        enableLabel = CustomFont_Label(canvasEnable, text=text, font_path=font_regular, size=16, bg=whitebg, width=210, height=30).grid(row=0, column=1, sticky='w')
        self.enabledCheck = Checkbutton(master=canvasEnable, width=9, font=small_font, height=2, variable=self.varEnabled, bd=0, anchor='e', bg=whitebg,
                                        activebackground=whitebg, highlightbackground=whitebg, highlightthickness=0)
        self.enabledCheck.grid(row=0, column=2)

        # Certificate line
        canvasCert = Canvas(secFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasCert.grid(row=1, column=0, sticky='w')
        certImg = Label(master=canvasCert, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Certificate:' + (100 - len(' Certificate:')) * " "
        certLabel = CustomFont_Label(canvasCert, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.certificate = Entry(master=canvasCert, text='test', width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.certificate.bind("<Button-1>", self.certificateInput)
        self.certificate.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        # Certificate Password line
        canvasPassw = Canvas(secFrame, bg='white', width=360, height=40, highlightcolor='white', bd=0)
        canvasPassw.grid(row=2, column=0, sticky='w')
        paswImg = Label(master=canvasPassw, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' Password:' + (100 - len(' Password:')) * " "
        paswLabel = CustomFont_Label(canvasPassw, text=text, font_path=font_regular, size=16, bg=whitebg, width=170).grid(row=1, column=1, sticky='w')
        self.secPaswText = Entry(master=canvasPassw, width=txtSize, font=small_font, bg=whitebg, show="*", bd=1)
        self.secPaswText.grid(row=1, column=2, sticky='w', pady=padY, padx=padX)

        secCanvas.place(x=0, y=510)

        canvasButton = tk.Canvas(self.canvas, width=52, height=4, bg='white', highlightcolor='white')
        canvasButton.place(x=0, y=615)
        button = CustomFont_Button(canvasButton, text="Log In", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, long=1, bg=buttonColor, highlightthickness=0, bd=0,
                                   height=45,
                                   width=380, activeforeground='white', activebackground=buttonColor,
                                   command=self.loginIn).grid(row=2)

    def protocolSelection(self, event):
        protocol = client_protocol.get_protocol_num(self.comboProtocol.get())
        self.login_refresh(protocol)

    def certificateInput(self, event):
        certificate_window_opened = False
        try:
            if self.app is not None:
                certificate_window_opened = self.app.opened
        except:
            pass

        if not certificate_window_opened:
            self.cert = Toplevel(root)
            self.cert.group(root)
            self.app = Certificate(self.cert, self)

    def willInput(self, event):
        will_window_opened = False
        try:
            if self.app is not None:
                will_window_opened = self.app.opened
        except:
            pass

        if not will_window_opened:
            self.will = Toplevel(root)
            self.will.group(root)
            self.app = Will(self.will, self)

    def close(self):
        try:
            self.certificate.delete(0, 'end')
        except AttributeError:
            pass
        self.main.login.withdraw()
        self.main.show_accounts()

    def loginIn(self):
        # create ACCOUNT and SAVE as default
        protocol = client_protocol.get_protocol_num(self.comboProtocol.get())
        name = self.nameText.get()
        password = self.paswText.get()
        clientID = self.idText.get()
        serverHost = self.hostText.get()
        serverPort = self.portText.get()
        cleanSession = self.varClean.get()
        keepAlive = self.keepText.get()
        will = self.willText.get()
        willT = self.willT.get()
        qos = self.comboQos.get()
        enabled = self.varEnabled.get()
        certificate = self.certificate.get()
        certPasw = self.secPaswText.get()

        if not certificate_validator.validate(certificate, certPasw):
            messagebox.showinfo("Warning", "certificate/password pair is invalid")
            return

        account = AccountEntity(protocol=protocol, username=name, password=password, clientID=clientID,
                                serverHost=serverHost,
                                port=serverPort, cleanSession=cleanSession, keepAlive=keepAlive, will=will,
                                willTopic=willT,
                                isRetain=True,
                                qos=qos, isDefault=False, isSecure=enabled, certificate=certificate, certPasw=certPasw)

        if AccountValidation.valid(account):
            d_manager = datamanager()
            previous = d_manager.get_account_clientID(account.clientID)
            if previous is None:
                d_manager.add_entity(account)
                d_manager.clear_default_account()
                d_manager.set_default_account_clientID(account.clientID)
                try:
                    self.certificate.delete(0, 'end')
                except AttributeError:
                    pass
                self.main.login.withdraw()
                self.main.show_loading(1000)
            else:
                messagebox.showinfo("Warning", "Wrong value for clientID='" + str(
                    account.clientID) + "'. This one is already in use")
        else:
            if account.keepAlive is '' or (int(account.keepAlive) <= 0 or int(account.keepAlive)) > 65535:
                messagebox.showinfo("Warning", 'Wrong value for Keepalive')
            elif not client_protocol.is_message_length_valid(account.protocol, len(account.will)):
                messagebox.showinfo("Warning", 'Will size/length is more than ' + str(client_protocol.get_max_message_length(account.protocol)) + ' symbols')
            else:
                messagebox.showinfo("Warning",
                                    'Please fill in all required fileds: Username, Password, ClientID, Host, Port')


class Certificate(Frame):

    def __init__(self, master, main):
        self.master = master
        center_child(self.master, 360, 325)
        self.master.resizable(False, False)
        master.title("Certificate")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        self.canvas = Canvas(self, bg='red', width=360, height=300, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.TextArea = Text(self.canvas, width=49)

        self.TextArea.insert(1.0, self.main.certificate.get())
        ScrollBar = Scrollbar(self.canvas)
        ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=ScrollBar.set)
        ScrollBar.pack(side=RIGHT, fill=Y)
        self.TextArea.pack(expand=YES, fill=BOTH)

        canvasButton = tk.Canvas(self.master, width=52, height=4)
        canvasButton.place(x=140, y=270)
        button = Button(canvasButton, text="OK", font=font.Font(family='Sans', size=12, weight="bold"), height=1, width=5, command=self.close).pack()

        self.opened = True

    def close(self):
        self.opened = False
        text = self.TextArea.get(1.0, END).rstrip()
        self.master.destroy()
        self.main.certificate.delete(0, END)
        self.main.certificate.insert(0, text)

    def destroy(self):
        self.opened = False
        super(Certificate, self).destroy()


class Will(Frame):

    def __init__(self, master, main):
        self.master = master
        center_child(self.master, 360, 325)
        self.master.resizable(False, False)
        master.title("Will")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        self.canvas = Canvas(self, bg='red', width=360, height=300, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.TextArea = Text(self.canvas, width=49)
        self.TextArea.insert(1.0, self.main.willText.get())

        ScrollBar = Scrollbar(self.canvas)
        ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=ScrollBar.set)
        ScrollBar.pack(side=RIGHT, fill=Y)
        self.TextArea.pack(expand=YES, fill=BOTH)

        canvasButton = tk.Canvas(self.master, width=52, height=4)
        canvasButton.place(x=140, y=270)
        button = Button(canvasButton, text="OK", font=font.Font(family='Sans', size=12, weight="bold"), height=1, width=5, command=self.close).pack(pady=20)

        self.opened = True

    def close(self):
        self.opened = False
        text = self.TextArea.get(1.0, END).rstrip()
        self.master.destroy()
        self.main.willText.delete(0, END)
        self.main.willText.insert(0, text)

    def destroy(self):
        self.opened = False
        super(Will, self).destroy()


class NoteForm(Frame):

    def __init__(self, master, main, active, old):
        self.master = master
        self.master.resizable(False, False)

        self.main = main
        Frame.__init__(self, master)
        self.grid()

        logo_panel(self.main.note)

        self.old = old

        self.note = ttk.Notebook(self, width=349, height=520)
        self.note.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        self.tab1 = Frame(self.note)
        self.tab2 = Frame(self.note)
        self.tab3 = Frame(self.note)
        self.tab4 = Frame(self.note)

        self.canvasTab1 = Canvas(self.tab1, bg=whitebg, width=349, height=520, bd=0, highlightthickness=0)
        self.canvasTab1.pack()
        self.canvasTab2 = Canvas(self.tab2, bg=whitebg, width=349, height=520, bd=0, highlightthickness=0)
        self.canvasTab2.pack()
        self.canvasTab3 = Canvas(self.tab3, bg=whitebg, width=349, height=520, bd=0, highlightthickness=0)
        self.canvasTab3.pack()

        self.photoimage0 = ImageTk.PhotoImage(Image.open("./resources/iot_broker_background.png"))
        self.canvasTab1.create_image(0, 0, anchor="nw", image=self.photoimage0)
        self.canvasTab2.create_image(0, 0, anchor="nw", image=self.photoimage0)
        self.canvasTab3.create_image(0, 0, anchor="nw", image=self.photoimage0)

        bold_font = ('Sans', 10, 'bold')

        gui_style = ttk.Style()
        gui_style.configure('TNotebook', tabposition='s')
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
        gui_style.configure('My.TCombobox', background=buttonColor, border=0, arrowcolor='white')

        delImage = Image.open('./resources/ic_delete_with_background.png')
        self.delPhoto = ImageTk.PhotoImage(delImage)

        self.refresh_all()

        if active == 0:
            self.note.add(self.tab1, image=self.main.topicsImgBlue)
        else:
            self.note.add(self.tab1, image=self.main.topicsImg)

        if active == 1:
            self.note.add(self.tab2, image=self.main.sendImgBlue)
        else:
            self.note.add(self.tab2, image=self.main.sendImg)

        if active == 2:
            self.note.add(self.tab3, image=self.main.messImgBlue)
        else:
            self.note.add(self.tab3, image=self.main.messImg)

        self.note.add(self.tab4, image=self.main.outImg)
        self.change_active_tab(active)
        self.note.grid(row=0, column=0)

        self.master.protocol("WM_DELETE_WINDOW", self._close)

    def change_active_tab(self, active_tab):
        self.active = active_tab
        self.note.select(self.active)

    def _on_mousewheel(self, event):
        scroll = 1 if event.num == 5 else -1
        self.messagesCanvas.yview_scroll(scroll, "units")

    def _close(self):
        self.master.destroy()
        self.main.master.deiconify()
        reactor.callFromThread(reactor.stop)

    def _destroy(self, event):
        self.messagesCanvas.unbind_all("<Button-4>")
        self.messagesCanvas.unbind_all("<Button-5>")

    def refresh_all(self):
        center_child(self.master, 355, 570)
        self.account = datamanager().get_default_account()
        protocol_text = client_protocol.get_protocol_name(self.account.protocol).upper()
        self.app = None
        self.master.title("iotbroker.cloud " + protocol_text)
        self.refresh_topics()
        self.refresh_send()
        self.refresh_messages()

    def refresh_tabs(self):
        if self.active == 0:
            self.note.tab(self.tab1, image=self.main.topicsImgBlue)
        else:
            self.note.tab(self.tab1, image=self.main.topicsImg)

        if self.active == 1:
            self.note.tab(self.tab2, image=self.main.sendImgBlue)
        else:
            self.note.tab(self.tab2, image=self.main.sendImg)

        if self.active == 2:
            self.note.tab(self.tab3, image=self.main.messImgBlue)
        else:
            self.note.tab(self.tab3, image=self.main.messImg)

    def refresh_send(self):
        size = 30
        txtSize = 18
        padY = 4
        padX = 5
        small_font = ('Sans', 11)
        bold_font = ('Sans', 10, 'bold')
        gui_style = ttk.Style()
        gui_style.configure('TNotebook', tabposition='s')
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
        gui_style.configure('My.TCombobox', background=buttonColor, border=0, arrowcolor='white')

        send = CustomFont_Label(self.canvasTab2, text=" send message:", font_path=font_bold, size=14).grid(row=0,
                                                                                                           sticky='w',
                                                                                                           pady=3)
        sendCanvas = tk.Canvas(self.canvasTab2, width=359, height=450, bg=whitebg, highlightcolor=whitebg)
        sendFrame = ttk.Frame(sendCanvas, style='My.TFrame')

        # Content line tab2
        canvasContent = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=whitebg, bd=0)
        canvasContent.grid(row=0, column=0, sticky='w')
        contentImg = Label(master=canvasContent, image=self.settingsPhoto, bd=0, height=size, width=size,
                           bg=whitebg).grid(row=0)

        text = ' Content:' + (100 - len(' Content:')) * " "
        contentLabel = CustomFont_Label(canvasContent, text=text, font_path=font_regular, size=16, bg=whitebg, width=140).grid(row=0, column=1, sticky='w')
        self.contentText = Entry(master=canvasContent, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.contentText.bind("<Button-1>", self.contentInput)
        self.contentText.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # Topic line tab2
        canvasTopic = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasTopic.grid(row=1, column=0, sticky='w')
        topicImg = Label(master=canvasTopic, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0)
        text = ' Topic:' + (100 - len(' Topic:')) * " "
        topicLabel = CustomFont_Label(canvasTopic, text=text, font_path=font_regular, size=16, bg=whitebg, width=140).grid(row=0, column=1, sticky='w')
        self.nameText2 = Entry(master=canvasTopic, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.nameText2.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # QoS line tab1
        canvasQos = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasQos.grid(row=2, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0)

        text = ' QoS:' + (100 - len(' QoS:')) * " "
        qosLabel = CustomFont_Label(canvasQos, text=text, font_path=font_regular, size=16, bg=whitebg, width=250).grid(row=0, column=1, sticky='w')

        datamanage = datamanager()

        self.comboQos2 = ttk.Combobox(master=canvasQos, values=client_protocol.qos_list(self.account.protocol), width=5, style='My.TCombobox', font=small_font)

        self.comboQos2.current(0)
        self.comboQos2.grid(row=0, column=2, sticky='e', pady=2)

        if client_protocol.publish_flags_enabled(self.account.protocol):
            self.varRetain = BooleanVar()
            self.varDuplicate = BooleanVar()

            # Retain line
            canvasRet = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
            canvasRet.grid(row=3, column=0, sticky='w')
            retainImg = Label(master=canvasRet, image=self.settingsPhoto, bd=0, height=size + 2, width=size, bg=whitebg).grid(row=0)

            text = ' Retain:' + (100 - len(' Retain:')) * " "
            retainLabel = CustomFont_Label(canvasRet, text=text, font_path=font_regular, size=16, bg=whitebg, width=210, height=30).grid(row=0, column=1, sticky='w')
            self.retainCheck = Checkbutton(master=canvasRet, height=2, width=9, font=small_font,
                                           variable=self.varRetain, bd=0, anchor='e', bg=whitebg,
                                           activebackground=graybg, highlightbackground=graybg,
                                           highlightthickness=0)
            self.retainCheck.grid(row=0, column=2, pady=2)

            # Duplicate line
            canvasDup = Canvas(sendFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
            canvasDup.grid(row=4, column=0, sticky='w')
            dupImg = Label(master=canvasDup, image=self.settingsPhoto, bd=0, height=size + 2, width=size, bg=whitebg).grid(row=0)
            text = ' Duplicate:' + (100 - len(' Duplicate:')) * " "
            dupLabel = CustomFont_Label(canvasDup, text=text, font_path=font_regular, size=16, bg=whitebg, width=210,
                                        height=30).grid(row=0, column=1, sticky='w')
            self.dupCheck = Checkbutton(master=canvasDup, height=2, width=9, font=small_font,
                                        variable=self.varDuplicate, bd=0, anchor='e', bg=whitebg,
                                        activebackground='white', highlightbackground=whitebg, highlightthickness=0)
            self.dupCheck.grid(row=0, column=2, pady=2)

        sendCanvas.create_window(0, 0, anchor='nw', window=sendFrame)
        sendCanvas.grid(row=1, column=0, sticky='eswn')

        canvasButton = tk.Canvas(self.canvasTab2, width=52, height=4, bg=whitebg, highlightcolor=whitebg)
        canvasButton.grid(row=2, column=0, sticky='eswn')

        button = CustomFont_Button(canvasButton, text="Send", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, long=2, offset_x=5, offset_y=-5, bg=buttonColor, highlightthickness=0, bd=0,
                                   height=45,
                                   width=380, activeforeground=whitebg, activebackground=buttonColor,
                                   command=self.sendTopic).grid(row=0, sticky='w')

    def contentInput(self, event):
        content_window_opened = False
        try:
            if self.app is not None:
                content_window_opened = self.app.opened
        except:
            pass

        if not content_window_opened:
            self.content = Toplevel(root)
            self.content.group(root)
            self.app = Content(self.content, self)

    def refresh_topics(self):
        small_font = ('Sans', 11)
        bold_font = ('Sans', 10, 'bold')
        gui_style = ttk.Style()
        gui_style.configure('TNotebook', tabposition='s')
        gui_style.configure('My.TFrame', background='white', border=0)
        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background='white')
        gui_style.configure('My.TCombobox', background=buttonColor, border=0, arrowcolor='white')

        self.topicIDs = []

        topics = CustomFont_Label(self.canvasTab1, text=" topics list:", font_path=font_bold, size=14).grid(row=0, sticky='w', pady=3)
        topicsCanvas = tk.Canvas(self.canvasTab1, width=340, height=350, bg=whitebg, highlightcolor=whitebg)
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
                        CustomFont_Label(topicsFrame, text=text, font_path=font_medium, size=16, width=230, bg=whitebg).grid(row=i + 1, column=0)
                        Label(master=topicsFrame, image=self.qosPhoto, bd=0, bg=whitebg).grid(row=i + 1, column=1,
                                                                                              sticky='w')
                        gui_style.configure('My.TLabel', border=0, font=bold_font, width=359, background=graybg)
                        ttk.Button(topicsFrame, image=self.delPhoto, text="Del", style='My.TLabel', command=lambda x=i: self.delete(x)).grid(row=i + 1, column=2, padx=5)
                    i += 1

        vbarTopics = ttk.Scrollbar(self.tab1, orient='vertical', command=topicsCanvas.yview)
        if i > 13:
            vbarTopics.place(x=335, y=30, height=350)
            vbarTopics.set(1, 1)
            topicsCanvas.configure(scrollregion=(0, 0, 349, 1000))

        topicsCanvas.create_window(0, 0, anchor='nw', window=topicsFrame)
        topicsCanvas.grid(row=1, column=0, sticky='eswn')

        newTopic = CustomFont_Label(self.canvasTab1, text=" add new topic:", font_path=font_bold, size=14).grid(row=2, sticky='w', pady=3)
        newCanvas = tk.Canvas(self.canvasTab1, width=349, height=70, bg=whitebg, highlightcolor=whitebg)
        newFrame = ttk.Frame(newCanvas, style='My.TFrame')

        settingsImage = Image.open('./resources/settings30.png')
        self.settingsPhoto = ImageTk.PhotoImage(settingsImage)

        size = 30
        txtSize = 18
        padY = 4
        padX = 5

        # Topic Name line tab1
        canvasName = Canvas(newFrame, bg=whitebg, width=360, height=40, highlightcolor=whitebg, bd=0)
        canvasName.grid(row=0, column=0, sticky='w')
        nameImg = Label(master=canvasName, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=0, column=0)

        text = ' Topic:' + (100 - len(' Topic:')) * " "
        nameLabel = CustomFont_Label(canvasName, text=text, font_path=font_regular, size=16, bg=whitebg, width=120).grid(row=0, column=1, sticky='w')
        self.nameText = Entry(master=canvasName, width=txtSize, font=small_font, bg=whitebg, bd=1)
        self.nameText.grid(row=0, column=2, sticky='w', pady=padY, padx=padX)

        # QoS line tab1
        canvasQos = Canvas(newFrame, bg=whitebg, width=360, height=40, highlightcolor=graybg, bd=0)
        canvasQos.grid(row=1, column=0, sticky='w')
        qosImg = Label(master=canvasQos, image=self.settingsPhoto, bd=0, height=size, width=size, bg=whitebg).grid(row=1, column=0)
        text = ' QoS:' + (100 - len(' QoS:')) * " "
        qosLabel = CustomFont_Label(canvasQos, text=text, font_path=font_regular, size=16, bg=whitebg, width=250).grid(row=1, column=1, sticky='w')
        self.comboQos = ttk.Combobox(master=canvasQos, values=client_protocol.qos_list(self.account.protocol), width=5, style='My.TCombobox', font=small_font)
        self.comboQos.current(0)
        self.comboQos.grid(row=1, column=2, sticky='e', pady=12)

        newCanvas.create_window(0, 0, anchor='nw', window=newFrame)
        newCanvas.grid(row=3, column=0, sticky='eswn')

        canvasButton = tk.Canvas(self.canvasTab1, width=52, height=4, bg='white', highlightcolor=whitebg)
        canvasButton.grid(row=4, column=0, sticky='eswn')

        button = CustomFont_Button(canvasButton, text="Add", foreground="white", font_path=font_bold,
                                   size=16, strings_number=1, long=2, offset_x=10, offset_y=-5, bg=buttonColor, highlightthickness=0, bd=0,
                                   height=45,
                                   width=360, activeforeground=whitebg, activebackground=buttonColor,
                                   command=self.createTopic).grid(row=0, sticky='w')

    def refresh_messages(self):
        messages = CustomFont_Label(self.canvasTab3, text=" messages list:", font_path=font_bold, size=14).grid(row=0, sticky='w', pady=3)
        self.messagesCanvas = tk.Canvas(self.canvasTab3, width=359, height=510, bg=whitebg, highlightcolor=whitebg)
        messagesFrame = ttk.Frame(self.messagesCanvas, style='My.TFrame')

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

        height = 0
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
                    strings_number = len(content) // 32 + 3
                    if strings_number > 3:
                        strings_number += 6
                        scroll_flag = True
                    if (i % 2) == 0:
                        CustomFont_Label(messagesFrame, text=text, font_path=font_regular, size=16,
                                         strings_number=strings_number, width=250, height=20 * strings_number,
                                         bg=whitebg).grid(row=i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg=whitebg).grid(row=i, column=1)
                    else:
                        CustomFont_Label(messagesFrame, text=text, font_path=font_regular, size=16,
                                         strings_number=strings_number, width=250, height=20 * strings_number,
                                         bg=graybg).grid(row=i, column=0)
                        Label(master=messagesFrame, image=self.photo, bd=0, bg=graybg, width=359 - 250, height=20 * strings_number + 2).grid(row=i, column=1)
                    i += 1
                    height += 20 * strings_number + 3

        if height == 0:
            height = 370

        vbarMessages = ttk.Scrollbar(self.tab3, orient='vertical', command=self.messagesCanvas.yview)
        if i > 8 or scroll_flag:
            vbarMessages.place(x=335, y=30, height=490)
            vbarMessages.set(1, 1)
            self.messagesCanvas.configure(scrollregion=(0, 0, 359, height))
        else:
            self.messagesCanvas.configure(scrollregion=(0, 0, 359, 490))

        self.messagesCanvas.create_window(0, 0, anchor='nw', window=messagesFrame)
        self.messagesCanvas.grid(row=1, column=0, sticky='eswn')

        self.bind("<Destroy>", self._destroy)
        self.messagesCanvas.bind_all("<Button-4>", self._on_mousewheel)
        self.messagesCanvas.bind_all("<Button-5>", self._on_mousewheel)

    def format_context(self, text):
        data = textwrap.wrap(text, 32)
        result = ''
        for piece in data:
            result += piece + '\n'
        return result

    def delete(self, id):
        # self.main.destroy()
        topicName = self.topicNames[id]
        # SEND UNSUBSCRIBE _________________________________________________________________________________SEND UNSUBSCRIBE
        self.main.client.unsubscribeFrom(topicName)

    def sendTopic(self):
        content = str.encode(self.contentText.get())
        name = self.nameText2.get()
        qos = self.comboQos2.get()
        retain = self.varRetain.get() if hasattr(self, "varRetain") else False
        dup = self.varDuplicate.get() if hasattr(self, "varDuplicate") else False
        self.contentText.text = ''
        self.nameText2 = ''
        self.comboQos.current(0)

        self.refresh_send()

        if client_protocol.is_udp(self.account.protocol) and len(content) > UDP_MAX_MESSAGE_LENGTH:
            messagebox.showinfo("Warning", 'Content size/length is more than ' + str(UDP_MAX_MESSAGE_LENGTH) + ' symbols')
            return

        # SEND PUBLISH _________________________________________________________________________________SEND PUBLISH
        contentDecoded = content.decode('utf8')
        self.main.client.publish(name, int(qos), contentDecoded, retain, dup)

        if int(qos) == 0:
            # ADD to DB
            datamanage = datamanager()
            account = datamanage.get_default_account()
            if account.protocol != 3:
                message = MessageEntity(content=content, qos=int(qos), topicName=name, incoming=False, isRetain=retain, isDub=dup, accountentity_id=account.id)
                datamanage.add_entity(message)
            self.main.app.refresh_messages()

    def createTopic(self):
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
                    self.nameText.text = '';
                    self.comboQos.current(0);
                self.main.client.subscribeTo(name, int(qos))
            else:
                self.nameText.text = '';
                self.comboQos.current(0);
                self.refresh_topics()
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
        self.active = new
        self.refresh_tabs()

        if new == 3:
            self.main.note.withdraw()
            self.main.show_accounts()
            # _____________________________________________________________________SEND___DISCONNECT
            if self.main.client is not None:
                self.main.client.disconnectWith(0)


class Content(Frame):

    def __init__(self, master, main):
        self.master = master
        center_child(self.master, 360, 325)
        self.master.resizable(False, False)
        master.title("Content")
        self.main = main
        Frame.__init__(self, master)
        self.grid()

        self.canvas = Canvas(self, bg='red', width=360, height=300, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.TextArea = Text(self.canvas, width=49)

        self.TextArea.insert(1.0, self.main.contentText.get())

        ScrollBar = Scrollbar(self.canvas)
        ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=ScrollBar.set)
        ScrollBar.pack(side=RIGHT, fill=Y)
        self.TextArea.pack(expand=YES, fill=BOTH)

        canvasButton = tk.Canvas(self.master, width=52, height=4)
        canvasButton.place(x=140, y=270)
        button = Button(canvasButton, text="OK", font=font.Font(family='Sans', size=12, weight="bold"), height=1, width=5, command=self.close).pack()

        self.opened = True

    def close(self):
        self.opened = False
        text = self.TextArea.get(1.0, END).rstrip()
        self.master.destroy()
        self.main.contentText.delete(0, END)
        self.main.contentText.insert(0, text)

    def destroy(self):
        self.opened = False
        super(Content, self).destroy()


logger = logging.getLogger('PIL')
logger.setLevel(level=logging.INFO)

UDP_MAX_MESSAGE_LENGTH = 1400

root = Tk()

logo = PhotoImage(file='./resources/iotbroker_icon_big.gif')
root.tk.call('wm', 'iconphoto', root._w, logo)

tksupport.install(root)
app = Main_screen(root)
reactor.run()
