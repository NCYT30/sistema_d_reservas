from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas import ServiceResponseModel, ServiceRequestModel, ServicePutModel
from ..database import Service

router = APIRouter(prefix='/service')

@router.get('/', response_model=List[ServiceResponseModel])
async def get_services(page: int = 1, limit: int = 10):
    services = Service.select()

    return [service for service in services]

@router.post('/', response_model=ServiceResponseModel)
async def create_service(service: ServiceRequestModel):
    new_service = Service.create(
        name=service.name,
        description=service.description,
        price=service.price,
        availability=service.availability
    )

    return new_service

@router.put('/{id}', response_model=ServiceResponseModel)
async def update_service(id: int, service_request: ServicePutModel):
    service = Service.select().where(Service.id == id).first()

    if service is None:
        raise HTTPException(status_code=404, detail='Servicio no encontrado')

    service.name = service_request.name
    service.description = service_request.description
    service.price = service_request.price
    service.availability = service_request.availability

    service.save()

    return service

@router.delete('/{id}', response_model=ServiceResponseModel)
async def delete_service(id: int):
    service = Service.select().where(Service.id == id).first()

    if service is None:
        raise HTTPException(status_code=404, detail='Servicio no encontrado')

    service.delete_instance()

    return service
