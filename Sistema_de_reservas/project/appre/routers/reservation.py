from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas import ReservationResponseModel, ReservationRequestModel, ReservationPutModel
from ..database import Reservation

router = APIRouter(prefix='/reservation')

@router.get('/', response_model=List[ReservationResponseModel])
async def get_reservations(page: int = 1, limit: int = 10):
    reservations = Reservation.select()

    return [reservation for reservation in reservations]

@router.post('/', response_model=ReservationResponseModel)
async def create_reservation(reservation: ReservationRequestModel):
    new_reservation = Reservation.create(
        user_id=reservation.user_id.id,
        service_id=reservation.service_id.id,
        date_time=reservation.date_time,
        status=reservation.status
    )

    return new_reservation

@router.put('/{id}', response_model=ReservationResponseModel)
async def update_reservation(id: int, reservation_request: ReservationPutModel):
    reservation = Reservation.select().where(Reservation.id == id).first()

    if reservation is None:
        raise HTTPException(status_code=404, detail='Reservación no encontrada')

    reservation.user_id = reservation_request.user_id.id
    reservation.service_id = reservation_request.service_id.id
    reservation.date_time = reservation_request.date_time
    reservation.status = reservation_request.status

    reservation.save()

    return reservation

@router.delete('/{id}', response_model=ReservationResponseModel)
async def delete_reservation(id: int):
    reservation = Reservation.select().where(Reservation.id == id).first()

    if reservation is None:
        raise HTTPException(status_code=404, detail='Reservación no encontrada')

    reservation.delete_instance()

    return reservation
