import json
import shutil

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import JSONResponse

from src.auth import AuthHandler

from src.models import (
    UserLoginModel,
    UserModel,
)

from src.db.userdbmanager import UserDatabaseManager

router = APIRouter(
    prefix='/auth',
    tags=['authentication'],
)

auth_handler = AuthHandler()
user_dm = UserDatabaseManager()


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
