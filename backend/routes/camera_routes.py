from fastapi import APIRouter
from controllers.camera_controller import start_camera, stop_camera, get_status

router = APIRouter(
    prefix="/camera",
    tags=["Camera"]
)

@router.post("/start")
def start():
    return start_camera()

@router.post("/stop")
def stop():
    return stop_camera()

@router.get("/status")
def status():
    return get_status()
