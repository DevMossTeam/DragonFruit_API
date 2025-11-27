from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Cek status perangkat
@router.get("/device-status")
def device_status():
    return {"status": "OK"}


# Model data yang dikirim dari ESP8266
class DevicePayload(BaseModel):
    weight: float
    grade: str

# Endpoint menerima data dari ESP8266
@router.post("/receive")
def receive_data(payload: DevicePayload):
    print("📩 Data diterima dari ESP8266:", payload)

    return {
        "message": "Data received successfully",
        "received": payload
    }
