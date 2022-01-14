# Routine Manager
Simple Routine Management API

## RUN (Local Development Server)
Configure with .env file - Create a .env file in app folder
```sh
# BASIC
DEBUG=
APP_HOST=
APP_PORT=

# DATABASE
MONGODB_USER=
MONGODB_PASS=
MONGODB_URL=
MONGODB_DB=

# JWT
SECRET_KEY=
ALGORITHM=
```
Install Dependencies
```sh
pip install -r requirements.txt
```
Run the App
```sh
python app.py
```
App is now running on desired host and port.
