from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app.models.fuel import Fuel
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.schemas.fuel import FuelCreate, FuelResponse
from app.dependencies import require_roles

router=APIRouter(tags=["Fuel"])

@router.post("/fuel",response_model=FuelResponse,status_code=201)
def create(data:FuelCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    if not db.get(Vehicle,data.vehicle_id):raise HTTPException(404,"Vehicle not found")
    if data.trip_id and not db.get(Trip,data.trip_id):raise HTTPException(404,"Trip not found")
    obj=Fuel(**data.model_dump(),total_cost=data.quantity*data.price_per_litre);db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/fuel",response_model=list[FuelResponse])
def list_fuel(page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=100),db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    return db.query(Fuel).offset((page-1)*limit).limit(limit).all()

@router.get("/vehicles/{vehicle_id}/fuel-history")
def history(vehicle_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    if not db.get(Vehicle,vehicle_id):raise HTTPException(404,"Vehicle not found")
    rows=db.query(Fuel).filter_by(vehicle_id=vehicle_id).all()
    return {"vehicle_id":vehicle_id,"total_expense":sum(x.total_cost for x in rows),"records":rows}

@router.get("/reports/fuel/monthly")
def monthly(db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    rows=db.query(extract("year",Fuel.fuel_date).label("year"),extract("month",Fuel.fuel_date).label("month"),func.sum(Fuel.total_cost).label("total")).group_by(extract("year",Fuel.fuel_date),extract("month",Fuel.fuel_date)).all()
    return [{"year":int(r.year),"month":int(r.month),"total":float(r.total or 0)} for r in rows]
