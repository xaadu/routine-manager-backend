from datetime import date, datetime
import json
import os
import shutil

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from src.auth import AuthHandler
from src.db.routinedbmanager import RoutineDatabaseManager

from src.models import (
    UserLoginModel,
    UserModel,
)

from src.db.userdbmanager import UserDatabaseManager

from .helper import get_routine_data

router = APIRouter(
    prefix='/auth',
    tags=['authentication'],
)

auth_handler = AuthHandler()
user_dm = UserDatabaseManager()
routine_dm = RoutineDatabaseManager()


@router.post('/login', response_description="JWT Authentication Token")
async def login(user_details: UserLoginModel):
    user = await user_dm.get_user(user_details.email)

    if user and user_details.password == user['password']:
        user = json.loads(UserModel(**user).json())
        token = auth_handler.encode_token(user.get('id'), user.get('email'))
        content = {'token': token}
    else:
        content = {'message': 'Invalid email or password'}
    
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@router.post('/upload', response_description="Upload Status", dependencies=[Depends(auth_handler.auth_wrapper)])
async def upload(file: UploadFile = File(...), effective_on: date = Form(...)):
    with open('routine.doc', 'wb') as f:
        shutil.copyfileobj(file.file, f)
    data = {
        'routine': get_routine_data('routine.doc'),
        'effective_on': datetime(effective_on.year, effective_on.month, effective_on.day)
    }
    os.remove('routine.doc')

    if await routine_dm.add_routine(data.copy()):
        data.update({'status': 'success'})
    else:
        data.update({'status': 'failed'})

    data.update({'effective_on': effective_on.strftime("%Y-%m-%d")})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)
