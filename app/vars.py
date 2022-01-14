import os
import urllib

APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
APP_PORT = int(os.environ.get('APP_PORT', '7004'))
DEBUG = os.environ.get('DEBUG', 'FALSE') == 'TRUE'

# DATABASE
MONGODB_USER = os.environ.get('MONGODB_USER')
MONGODB_PASS = urllib.parse.quote(os.environ.get('MONGODB_PASS'))
MONGODB_URL = os.environ.get('MONGODB_URL')
MONGODB_DB = os.environ.get('MONGODB_DB')
MONGODB_CONNECTION_STRING = f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_URL}/{MONGODB_DB}?retryWrites=true&w=majority'
