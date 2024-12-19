from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException

class DeviceStatusRequest(BaseModel):
   status : str

# Вместо базы данных
device_statuses = {}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Devices online"}

@app.put("/devices/{device_id}/status")
async def set_device_status(device_status_request : DeviceStatusRequest, device_id : int):
    
    if device_status_request.status not in ["on", "off"]:
        raise HTTPException( status_code=404, detail="Expected statuses are: on, off" )

    device_statuses[device_id] = device_status_request.status

@app.get("/devices/{device_id}/status")
async def get_device_status(device_id : int):

    if device_id not in device_statuses:
        raise HTTPException( status_code=404, detail="No device" )

    return JSONResponse( {"device": device_id, "status": device_statuses.get(device_id)} )
