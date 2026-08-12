from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse
from app.dependencies import require_roles

router=APIRouter(prefix="/drivers",tags=["Drivers"])

@router.post("",response_model=DriverResponse,status_code=201)
def create(data:DriverCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    if data.license_expiry < date.today(): raise HTTPException(400,"License expiry date must be in the future")
    if db.query(Driver).filter_by(license_number=data.license_number).first(): raise HTTPException(409,"License number already exists")
    obj=Driver(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("")
def list_drivers(name:str|None=None,status:str|None=None,page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=100),db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    q=db.query(Driver)
    if name:q=q.filter(Driver.name.ilike(f"%{name}%"))
    if status:q=q.filter(Driver.status==status)
    total=q.count(); data=q.offset((page-1)*limit).limit(limit).all()
    return {"total_records":total,"current_page":page,"limit":limit,"data":data}

@router.get("/{driver_id}",response_model=DriverResponse)
def get(driver_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    obj=db.get(Driver,driver_id)
    if not obj:raise HTTPException(404,"Driver not found")
    return obj

@router.put("/{driver_id}",response_model=DriverResponse)
def update(driver_id:int,data:DriverUpdate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    obj=db.get(Driver,driver_id)
    if not obj:raise HTTPException(404,"Driver not found")
    if data.license_expiry and data.license_expiry < date.today():raise HTTPException(400,"License expiry date must be in the future")
    for k,v in data.model_dump(exclude_unset=True).items():setattr(obj,k,v)
    db.commit();db.refresh(obj);return obj
