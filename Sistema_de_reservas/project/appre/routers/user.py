from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends, status

from passlib.context import CryptContext
from passlib.hash import bcrypt


from ..schemas import UserResponseModel
from ..schemas import UserRequestModel
from ..schemas import UserRequestPutModel

from ..database import User

router = APIRouter(prefix= '/users')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/', response_model = list[UserResponseModel])
async def get_user(page: int = 1, limit: int = 10):
    users =  User.select()

    return [ user for user in users ]



@router.post('/', response_model = UserResponseModel)
async def create_user(user: UserRequestModel):

    hashed_password = bcrypt.hash(user.password)

    user = User.create(
        name = user.name,
        email = user.email,
        password = hashed_password
    )

    return user


@router.put('/{id}', response_model = UserResponseModel)
async def update_user(id: int, user_request: UserRequestPutModel):

    user = User.select().where(User.id == id).first()

    if user is None:
        raise HTTPException(status_code = 404, detail = 'Usuario no encontrado')

    
    user.name = user_request.name
    user.email = user_request.email
    user.password = user_request.password

    user.save()

    return user


@router.delete('/{id}', response_model = UserResponseModel)
async def delete_user(id: int):

    user = User.select().where(User.id == id).first()

    if user is None:
        raise HTTPException(status_code = 404, detail = 'Usuario no encontrado')

    user.delete_instance()

    return user


def get_password_hash(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return pwd_context.hash(password)