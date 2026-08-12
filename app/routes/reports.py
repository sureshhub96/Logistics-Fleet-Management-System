from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.fuel import Fuel
from app.models.maintenance import Maintenance
from app.dependencies import require_roles

router=APIRouter(prefix="/reports",tags=["Dashboard & Reports"])

@router.get("/dashboard")
def dashboard(db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    return {
      "total_vehicles":db.query(Vehicle).count(),
      "available_vehicles":db.query(Vehicle).filter_by(status="Available").count(),
      "vehicles_under_maintenance":db.query(Vehicle).filter_by(status="Maintenance").count(),
      "total_drivers":db.query(Driver).count(),
      "active_drivers":db.query(Driver).filter_by(status="Active").count(),
      "total_trips":db.query(Trip).count(),
      "completed_trips":db.query(Trip).filter_by(trip_status="Delivered").count(),
      "cancelled_trips":db.query(Trip).filter_by(trip_status="Cancelled").count(),
      "total_fuel_expenses":float(db.query(func.coalesce(func.sum(Fuel.total_cost),0)).scalar()),
      "total_maintenance_expenses":float(db.query(func.coalesce(func.sum(Maintenance.service_cost),0)).scalar())
    }

@router.get("/vehicle/{vehicle_id}/expenses")
def vehicle_expenses(vehicle_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    fuel=float(db.query(func.coalesce(func.sum(Fuel.total_cost),0)).filter(Fuel.vehicle_id==vehicle_id).scalar())
    maintenance=float(db.query(func.coalesce(func.sum(Maintenance.service_cost),0)).filter(Maintenance.vehicle_id==vehicle_id).scalar())
    return {"vehicle_id":vehicle_id,"fuel_expense":fuel,"maintenance_expense":maintenance,"total_expense":fuel+maintenance}

@router.get("/driver/{driver_id}/trips")
def driver_trips(driver_id:int,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Fleet Manager"))):
    rows=db.query(Trip).filter(Trip.driver_id==driver_id).all()
    return {"driver_id":driver_id,"total_trips":len(rows),"completed_trips":sum(t.trip_status=="Delivered" for t in rows),"trips":rows}
