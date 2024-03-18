from fastapi import FastAPI
from fastapi import APIRouter

from .database import User
from .database import Service
from .database import Reservation
from .database import Notification

from .routers import user_router
from .routers import notification_router
from .routers import service_router
from .routers import reservation_router

from .database import database as connection

app = FastAPI(title = 'Sistema de reservas')


api_v1 = APIRouter(prefix = '/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(notification_router)
api_v1.include_router(service_router)
api_v1.include_router(reservation_router)

app.include_router(api_v1)


@app.on_event('startup')
def startup():
  if connection.is_closed():
      connection.connect()

  connection.create_tables([User, Service, Reservation, Notification])


@app.on_event('shutdown')
def shutdown():
  if not connection.is_closed():
      connection.close()