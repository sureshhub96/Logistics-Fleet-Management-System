from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine

# Import all models before create_all
import app.models

from app.routes.auth import router as auth_router
from app.routes.vehicles import router as vehicle_router
from app.routes.drivers import router as driver_router
from app.routes.trips import router as trip_router
from app.routes.fuel import router as fuel_router
from app.routes.maintenance import router as maintenance_router
from app.routes.reports import router as reports_router


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Logistics & Fleet Management System",
    version="1.0.0"
)


app.include_router(
    auth_router
)

app.include_router(
    vehicle_router
)

app.include_router(
    driver_router
)

app.include_router(
    trip_router
)

app.include_router(
    fuel_router
)

app.include_router(
    maintenance_router
)

app.include_router(
    reports_router
)


@app.get("/")
def root():

    return {
        "message": "Logistics & Fleet Management System is running",
        "docs": "/docs"
    }


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    print("\n================ ERROR ================")
    print("PATH:", request.url.path)
    print("ERROR TYPE:", type(exc).__name__)
    print("ERROR:", repr(exc))
    print("========================================\n")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )