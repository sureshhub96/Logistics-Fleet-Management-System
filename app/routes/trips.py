from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.tracking import Tracking
from app.schemas.trip import TripCreate, TripResponse, TrackingCreate, TrackingResponse
from app.dependencies import require_roles

router=APIRouter(prefix="/trips",tags=["Trips"])

def add_tracking(db,trip,status,remarks="Status update"):
    db.add(Tracking(trip_id=trip.id,location=trip.destination if status=="Delivered" else trip.source,status=status,remarks=remarks,timestamp=datetime.now(timezone.utc)))

@router.post("",response_model=TripResponse,status_code=201)
def create(data:TripCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    v=db.get(Vehicle,data.vehicle_id); d=db.get(Driver,data.driver_id)
    if not v or not d:raise HTTPException(404,"Vehicle or driver not found")
    if v.status in ("Maintenance","Inactive","Assigned"):raise HTTPException(400,"Vehicle is not available")
    if d.status!="Active" or d.license_expiry < datetime.now().date():raise HTTPException(400,"Driver is inactive or license is expired")
    active= ("Scheduled","Started","In Transit")
    if db.query(Trip).filter(Trip.vehicle_id==v.id,Trip.trip_status.in_(active)).first():raise HTTPException(400,"Vehicle already has an active trip")
    if db.query(Trip).filter(Trip.driver_id==d.id,Trip.trip_status.in_(active)).first():raise HTTPException(400,"Driver already has an active trip")
    obj=Trip(**data.model_dump());db.add(obj);db.flush();v.status="Assigned";add_tracking(db,obj,"Scheduled","Trip scheduled");db.commit();db.refresh(obj);return obj

@router.get("")
def list_trips(status:str|None=None,source:str|None=None,destination:str|None=None,trip_date:str|None=None,page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=100),db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    q=db.query(Trip)
    if status:q=q.filter(Trip.trip_status==status)
    if source:q=q.filter(Trip.source.ilike(f"%{source}%"))
    if destination:q=q.filter(Trip.destination.ilike(f"%{destination}%"))
    if trip_date:q=q.filter(Trip.start_date.cast(str).like(f"{trip_date}%"))
    total=q.count();data=q.offset((page-1)*limit).limit(limit).all()
    return {"total_records":total,"current_page":page,"limit":limit,"data":data}

@router.get("/{trip_id}",response_model=TripResponse)
def get(trip_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    obj=db.get(Trip,trip_id)
    if not obj:raise HTTPException(404,"Trip not found")
    return obj

def change_status(trip_id,status,db):
    obj=db.get(Trip,trip_id)
    if not obj:raise HTTPException(404,"Trip not found")
    if obj.trip_status in ("Delivered","Cancelled"):raise HTTPException(400,"Trip is already closed")
    obj.trip_status=status
    if status=="Delivered": obj.vehicle.status="Available"; obj.vehicle.current_km=max(obj.vehicle.current_km, obj.distance)
    elif status=="Cancelled": obj.vehicle.status="Available"
    else: obj.vehicle.status="Assigned"
    add_tracking(db,obj,status)
    db.commit();db.refresh(obj);return obj

@router.put("/{trip_id}/start",response_model=TripResponse)
def start(trip_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):return change_status(trip_id,"Started",db)

@router.put("/{trip_id}/complete",response_model=TripResponse)
def complete(trip_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):return change_status(trip_id,"Delivered",db)

@router.put("/{trip_id}/cancel",response_model=TripResponse)
def cancel(trip_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):return change_status(trip_id,"Cancelled",db)

@router.post("/{trip_id}/tracking",response_model=TrackingResponse,status_code=201)
def tracking(trip_id:int,data:TrackingCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    trip=db.get(Trip,trip_id)
    if not trip:raise HTTPException(404,"Trip not found")
    if trip.trip_status=="Delivered":raise HTTPException(400,"Completed trips cannot receive tracking updates")
    obj=Tracking(trip_id=trip_id,location=data.location,status=data.status,remarks=data.remarks,timestamp=datetime.now(timezone.utc))
    if data.status != trip.trip_status:
        trip.trip_status=data.status
        if data.status=="Delivered":trip.vehicle.status="Available"
    db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/{trip_id}/tracking",response_model=list[TrackingResponse])
def tracking_history(trip_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager","Driver"))):
    if not db.get(Trip,trip_id):raise HTTPException(404,"Trip not found")
    return db.query(Tracking).filter_by(trip_id=trip_id).order_by(Tracking.timestamp).all()
