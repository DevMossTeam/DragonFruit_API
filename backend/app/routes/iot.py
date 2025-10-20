from fastapi import APIRouter

router = APIRouter()

@router.post("/update-status")
def update_status(device_id: str, status: str):
    return {"device_id": device_id, "status": status}
