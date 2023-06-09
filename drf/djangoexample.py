import sys
from django.core.management import execute_from_command_line
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamam_settings.settings')

def runserver():
    host = '0.0.0.0'
    port = 8000
    sys.argv = ['manage.py', 'runserver', f'{host}:{port}']
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    runserver()
