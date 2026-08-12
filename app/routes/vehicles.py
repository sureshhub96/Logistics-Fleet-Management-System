from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.dependencies import require_roles

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("", response_model=VehicleResponse, status_code=201)
def create(data: VehicleCreate, db: Session = Depends(get_db), _=Depends(require_roles("Admin","Fleet Manager"))):
    if db.query(Vehicle).filter_by(vehicle_number=data.vehicle_number).first():
        raise HTTPException(409, "Vehicle number already exists")
    obj = Vehicle(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("")
def list_vehicles(status: str|None=None, vehicle_type: str|None=None, page: int=Query(1,ge=1), limit: int=Query(10,ge=1,le=100), db: Session=Depends(get_db), _=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    q=db.query(Vehicle)
    if status: q=q.filter(Vehicle.status==status)
    if vehicle_type: q=q.filter(Vehicle.vehicle_type.ilike(f"%{vehicle_type}%"))
    total=q.count(); data=q.offset((page-1)*limit).limit(limit).all()
    return {"total_records":total,"current_page":page,"limit":limit,"data":data}

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get(vehicle_id:int, db:Session=Depends(get_db), _=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    obj=db.get(Vehicle,vehicle_id)
    if not obj: raise HTTPException(404,"Vehicle not found")
    return obj

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update(vehicle_id:int, data:VehicleUpdate, db:Session=Depends(get_db), _=Depends(require_roles("Admin","Fleet Manager"))):
    obj=db.get(Vehicle,vehicle_id)
    if not obj: raise HTTPException(404,"Vehicle not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@router.delete("/{vehicle_id}")
def delete(vehicle_id:int, db:Session=Depends(get_db), _=Depends(require_roles("Admin"))):
    obj=db.get(Vehicle,vehicle_id)
    if not obj: raise HTTPException(404,"Vehicle not found")
    if obj.status=="Assigned": raise HTTPException(400,"Assigned vehicle cannot be deleted")
    db.delete(obj); db.commit(); return {"message":"Vehicle deleted"}
