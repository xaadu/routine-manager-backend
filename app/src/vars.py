import os

APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
APP_PORT = int(os.environ.get('APP_PORT', '7004'))
DEBUG = os.environ.get('DEBUG', 'FALSE') == 'TRUE'
