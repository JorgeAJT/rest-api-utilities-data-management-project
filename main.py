import uvicorn
from fastapi import FastAPI
from src import api_router

app = FastAPI(title="rest-api-utilities-data-management-project")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
