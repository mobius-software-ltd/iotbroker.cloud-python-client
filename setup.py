import subprocess
import os

#Input password for sudo________________!!!IMPORTANT!!!DONT FORGET!!!
sudoPassword = 'INPUT PASSWORD'
command = 'pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

subprocess.check_call(['pip', 'install', 'SQLAlchemy'])
subprocess.check_call(['pip', 'install', 'autobahn[twisted]'])
subprocess.check_call(['pip', 'install', 'numpy'])
#subprocess.check_call(['pip', 'install', 'pyopenssl or pip install pyOpenSSL==18.0.0'])
subprocess.check_call(['pip', 'install', 'pyopenssl'])
subprocess.check_call(['pip', 'install', 'service_identity'])
subprocess.check_call(['pip', 'install', 'pem'])
subprocess.check_call(['pip', 'install', 'python3-dtls'])


