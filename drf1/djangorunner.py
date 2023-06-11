import os
import sys
from django.core.management import execute_from_command_line
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CONFIG_DIR)
from config import host, port

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamam_settings.settings')

def runserver():
    #host = host
    #port = port
    sys.argv = ['manage.py', 'runserver', f'{host}:{port}']
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    runserver()
