import subprocess
import os

subprocess.check_call(['pip3', 'install', '-U', '-f','https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04', 'wxPython'])
subprocess.check_call(['pip3', 'install', 'SQLAlchemy'])
subprocess.check_call(['pip3', 'install', 'autobahn[twisted]'])
subprocess.check_call(['pip3', 'install', 'numpy'])
subprocess.check_call(['pip3', 'install', 'cryptography'])
subprocess.check_call(['pip3', 'install', 'pyOpenSSL'])
subprocess.check_call(['pip3', 'install', 'service_identity'])
subprocess.check_call(['pip3', 'install', 'pem'])
subprocess.check_call(['pip3', 'install', 'python3-dtls'])


