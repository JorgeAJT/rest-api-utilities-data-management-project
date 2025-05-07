import uvicorn
from fastapi import FastAPI
from src import api_router

app = FastAPI(
    title="rest-api-utilities-data-management-project",
    version="0.1.0",
    openapi_tags=[
        {"name": "mandate_data",   "description": "Mandate Data Operations"},
        {"name": "meter_data",     "description": "Meter Data Operations"},
        {"name": "meter_readings", "description": "Meter Readings Operations"},
    ],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
