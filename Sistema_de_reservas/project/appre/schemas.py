from typing import Any 

from datetime import date

from pydantic import validator
from pydantic import BaseModel

from pydantic.utils import GetterDict

from peewee import ModelSelect

class PeeWeeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res 


class ResponseModel(BaseModel):

    class Config:
        orm_mode = True
        getter_dict = PeeWeeGetterDict




#--------User---------------------------

class UserValidator:

    @validator('name')
    def name_validator(cls, name):
        if len(name) < 3 or len(name) > 25:
            raise ValueError('El rango para escribir el nombre es de 3 a 25 caracteres')
        return name 

    @validator('email')
    def email_validator(cls, email):
        if len(email) < 6 or len(email) > 35:
            raise ValueError('El rango para escribir el correo es de 6 a 35 caracteres')
        return email

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 8 or len(password) > 50:
            raise ValueError('Necesita como minimo 8 caracteres')
        return password


class UserResponseModel(ResponseModel):
    id: int
    name: str
    email: str
    password: str


class UserRequestModel(BaseModel, UserValidator):
    name: str
    email: str
    password: str


class UserRequestPutModel(BaseModel, UserValidator):
    name: str
    email: str
    password: str



#-----------Notification----------

class NotificationResponseModel(ResponseModel):
    user_id: UserResponseModel
    message: str
    sent_date: str


class NotificationRequestModel(BaseModel):
    user_id: UserResponseModel
    message: str
    sent_date: str


class NotificationRequestPutModel(BaseModel):
    user_id: UserResponseModel
    message: str
    sent_date: str



#---------------Service-------------------

class ServiceResponseModel(ResponseModel):
    id: int
    name: str
    description: str
    price: int
    availability: int


class ServiceRequestModel(BaseModel):
    name: str
    description: str
    price: int
    availability: int


class ServicePutModel(BaseModel):
    name: str
    description: str
    price: int
    availability: int


#---------Reservation--------------


class ReservationResponseModel(ResponseModel):
    user_id: UserResponseModel
    service_id: ServiceResponseModel
    date_time: str
    status: int


class ReservationRequestModel(ResponseModel):
    user_id: UserResponseModel
    service_id: ServiceResponseModel
    date_time: str
    status: int


class ReservationPutModel(ResponseModel):
    user_id: UserResponseModel
    service_id: ServiceResponseModel
    date_time: str
    status: int