# iotbroker.cloud-python-client

### Project description

IoTBroker.cloud Python Client is an application that allows you to connect to the server using MQTT, MQTT-SN, 
AMQP or COAP protocols. IoTBroker.cloud Python Client gives the opportunity to exchange messages using protocols 
mentioned above. Your data can be also encrypted with **TLS** or **DTLS** secure protocols.   

Below you can find a brief description of each protocol that can help you make your choice. 
If you need to get more information, you can find it in our [blog](https://www.iotbroker.cloud/clientApps/Python/MQTT).
 
**MQTT** is a lightweight publish-subscribe based messaging protocol built for use over TCP/IP.  
MQTT was designed to provide devices with limited resources an easy way to communicate effectively. 
You need to familiarize yourself with the following MQTT features such as frequent communication drops, low bandwidth, 
low storage and processing capabilities of devices. 

Frankly, **MQTT-SN** is very similar to MQTT, but it was created for avoiding the potential problems that may occur at WSNs. 

Creating large and complex systems is always associated with solving data exchange problems between their various nodes. 
Additional difficulties are brought by such factors as the requirements for fault tolerance, 
he geographical diversity of subsystems, the presence a lot of nodes interacting with each others. 
The **AMQP** protocol was developed to solve all these problems, which has three basic concepts: 
exchange, queue and routing key. 

If you need to find a simple solution, it is recommended to choose the **COAP** protocol. 
The CoAP is a specialized web transfer protocol for use with constrained nodes and constrained (e.g., low-power, lossy) 
networks. It was developed to be used in very simple electronics devices that allows them to communicate interactively 
over the Internet. It is particularly targeted for small low power sensors, switches, valves and similar components 
that need to be controlled or supervised remotely, through standard Internet networks.   
 
### Prerequisites 
[PyCharm](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux&code=PCC) should be installed
before starting to clone IoTBroker.Cloud Python Client. 

### Installation 
* First, you should download iotbroker.cloud-python-client. 

* Then you should open PyCharm, previously installed, and create a new project. 
You should go to **File > New Project > Create> Open in New window** . 

* Then you should extract and copy files from the iotbroker.cloud-python-client folder. 
After that you should open ‘PyCharm Projects’ on your PC (most probably, this folder will be saved in Home),
find there is the created project in PyCharm and select *‘Venv’ folder* to copy there the iotbroker.cloud-python-client files.

* Now you should install [wxPython - 4.0.3.](https://wxpython.org/). Open the terminal window in PyCharm and run 
the following command: 
```
pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython
```

* Next you should install [SQLAlchemy-1.2.14.](https://www.sqlalchemy.org/). Open the terminal window in PyCharm 
and run the following command: 
```
pip install SQLAlchemy
```
* Then you should install  [autobahn-18.11.1.](https://autobahn.readthedocs.io/en/latest/installation.html).
Open the terminal window in PyCharm and run the following command: 

```
pip install autobahn[twisted]
```

* Then you should install [NumPy-1.15.4.](http://www.numpy.org/). Open the terminal window in PyCharm and run the following command: 

```
pip install numpy
```

In case of successful installation, you can launch IoTBroker.Cloud. In order to start the application, you should set 
the cursor on the GUI_wx.py and right-click **Run ‘GUI_wx.py’**. If the procedure is successful, you will see 
the Login page in the form of pop-up window. Now you can log in and start exchanging messages with server. 
 
Please note that at this stage it is not possible to register as a client. You can only log in to your existing account. 

IoTBroker.Cloud C Client is developed by [Mobius Software](http://mobius-software.com/).

## [License](LICENSE.md)
