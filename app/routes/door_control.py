"""
Door control endpoints
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.schemas import DoorControlResponse
from app.config.logger import logger

router = APIRouter(tags=["Door Control"], prefix="/door")


# In-memory door state (in production, use a database or hardware control)
_door_state = {"locked": True}


@router.post("/lock", response_model=DoorControlResponse)
async def lock_door():
    """
    Lock the door
    
    Returns:
        DoorControlResponse with status
    """
    try:
        _door_state["locked"] = True
        logger.info("Door locked")
        return DoorControlResponse(
            action="lock",
            status="success",
            locked=True,
            message="Door locked successfully"
        )
    except Exception as e:
        logger.error(f"Error locking door: {e}")
        return JSONResponse(
            {
                "error": "Failed to lock door",
                "details": str(e),
                "status_code": 500
            },
            status_code=500
        )


@router.post("/unlock", response_model=DoorControlResponse)
async def unlock_door():
    """
    Unlock the door
    
    Returns:
        DoorControlResponse with status
    """
    try:
        _door_state["locked"] = False
        logger.info("Door unlocked")
        return DoorControlResponse(
            action="unlock",
            status="success",
            locked=False,
            message="Door unlocked successfully"
        )
    except Exception as e:
        logger.error(f"Error unlocking door: {e}")
        return JSONResponse(
            {
                "error": "Failed to unlock door",
                "details": str(e),
                "status_code": 500
            },
            status_code=500
        )


@router.get("/status", response_model=DoorControlResponse)
async def get_door_status():
    """
    Get current door status
    
    Returns:
        DoorControlResponse with current status
    """
    try:
        locked = _door_state.get("locked", True)
        logger.info(f"Door status requested: locked={locked}")
        return DoorControlResponse(
            action="status",
            status="success",
            locked=locked,
            message="Door is " + ("locked" if locked else "unlocked")
        )
    except Exception as e:
        logger.error(f"Error getting door status: {e}")
        return JSONResponse(
            {
                "error": "Failed to get door status",
                "details": str(e),
                "status_code": 500
            },
            status_code=500
        )
