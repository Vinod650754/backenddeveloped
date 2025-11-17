"""
Door control endpoints
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config.logger import logger

router = APIRouter(tags=["Door Control"], prefix="/door")


# In-memory door state (in production, use a database or hardware control)
_door_state = {"locked": True}


@router.post("/lock")
async def lock_door():
    """
    Lock the door
    
    Returns:
        JSON response with status
    """
    try:
        _door_state["locked"] = True
        logger.info("Door locked")
        return JSONResponse(
            {
                "action": "lock",
                "status": "success",
                "locked": True,
                "message": "Door locked successfully"
            },
            status_code=200
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


@router.post("/unlock")
async def unlock_door():
    """
    Unlock the door
    
    Returns:
        JSON response with status
    """
    try:
        _door_state["locked"] = False
        logger.info("Door unlocked")
        return JSONResponse(
            {
                "action": "unlock",
                "status": "success",
                "locked": False,
                "message": "Door unlocked successfully"
            },
            status_code=200
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


@router.get("/status")
async def get_door_status():
    """
    Get current door status
    
    Returns:
        JSON response with current status
    """
    try:
        locked = _door_state.get("locked", True)
        logger.info(f"Door status requested: locked={locked}")
        return JSONResponse(
            {
                "action": "status",
                "status": "success",
                "locked": locked,
                "message": "Door is " + ("locked" if locked else "unlocked")
            },
            status_code=200
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
