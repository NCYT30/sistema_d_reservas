from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends, status

from passlib.context import CryptContext
from passlib.hash import bcrypt


from ..schemas import NotificationResponseModel
from ..schemas import NotificationRequestModel
from ..schemas import NotificationRequestPutModel

from ..database import Notification

router = APIRouter(prefix= '/notification')


@router.get('/', response_model = list[NotificationResponseModel])
async def get_notification(page: int = 1, limit: int = 10):

    notifi = Notification.select()

    return [ noti for noti in notifi ]



@router.post('/', response_model = NotificationResponseModel)
async def create_notification(notifi: NotificationRequestModel):

    notifi = Notification.create(
        user_id = notifi.user_id.id,
        message = notifi.message,
        sent_date = notifi.sent_date
    )

    return notifi


@router.put('/{id}', response_model = NotificationResponseModel)
async def update_notification(id: int, notifi_request: NotificationRequestPutModel):

    noti = Notification.select().where(Notification.id == id).first()


    if noti is None:
        raise HTTPException(status_code = 404, detail = 'Notificacion no encontrada')

    noti.user_id = notifi_request.user_id.id
    noti.message = notifi_request.message
    noti.sent_date = notifi_request.sent_date

    noti.save()

    return noti


@router.delete('/{id}', response_model = NotificationResponseModel)
async def delete_notification(id: int):
    
    noti = Notification.select().where(Notification.id == id).first()

    if noti is None:
        raise HTTPException(status_code = 404, detail = 'Notificacion no encontrado')

    noti.delete_instance()

    return noti
