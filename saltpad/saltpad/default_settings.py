import os
import sys
reload(sys)  # Reload is a hack
sys.setdefaultencoding('UTF8')

API_URL = "http://172.27.102.38:8000/"
SECRET_KEY = os.urandom(24)
LOG_FILE = "saltpad.log"
HOST = "127.0.0.1"
EAUTH = "pam"

