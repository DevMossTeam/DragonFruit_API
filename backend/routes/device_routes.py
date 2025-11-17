from fastapi import APIRouter

router = APIRouter()

@router.get("/device-status")
def device_status():
    return {"status": "OK"}
