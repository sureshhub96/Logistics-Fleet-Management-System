from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.maintenance import Maintenance
from app.models.vehicle import Vehicle
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from app.dependencies import require_roles

router=APIRouter(tags=["Maintenance"])

@router.post("/maintenance",response_model=MaintenanceResponse,status_code=201)
def create(data:MaintenanceCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    v=db.get(Vehicle,data.vehicle_id)
    if not v:raise HTTPException(404,"Vehicle not found")
    if data.status=="In Progress":v.status="Maintenance"
    obj=Maintenance(**data.model_dump());db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/maintenance",response_model=list[MaintenanceResponse])
def list_all(db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):return db.query(Maintenance).all()

@router.get("/vehicles/{vehicle_id}/maintenance",response_model=list[MaintenanceResponse])
def vehicle_history(vehicle_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    if not db.get(Vehicle,vehicle_id):raise HTTPException(404,"Vehicle not found")
    return db.query(Maintenance).filter_by(vehicle_id=vehicle_id).all()

@router.put("/maintenance/{maintenance_id}",response_model=MaintenanceResponse)
def update(maintenance_id:int,data:MaintenanceUpdate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    obj=db.get(Maintenance,maintenance_id)
    if not obj:raise HTTPException(404,"Maintenance record not found")
    for k,v in data.model_dump(exclude_unset=True).items():setattr(obj,k,v)
    if obj.status=="In Progress":obj.vehicle.status="Maintenance"
    elif obj.status=="Completed":
        obj.vehicle.status="Available";obj.vehicle.current_km=max(obj.vehicle.current_km,obj.current_km)
    db.commit();db.refresh(obj);return obj

@router.get("/reports/maintenance/monthly")
def monthly(db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    from sqlalchemy import extract,func
    rows=db.query(extract("year",Maintenance.service_date).label("year"),extract("month",Maintenance.service_date).label("month"),func.sum(Maintenance.service_cost).label("total")).group_by(extract("year",Maintenance.service_date),extract("month",Maintenance.service_date)).all()
    return [{"year":int(r.year),"month":int(r.month),"total":float(r.total or 0)} for r in rows]
