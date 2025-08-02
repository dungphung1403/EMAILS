from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
import base64

router = APIRouter(prefix="/track", tags=["tracking"])

@router.get("/email/{meeting_id}/{user_id}")
async def track_email_read(
    meeting_id: int,
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Track email read event and return 1x1 transparent pixel image.
    This endpoint is called when an email is opened via an embedded tracking pixel.
    """
    
    # Check if meeting exists
    meeting = crud.get_meeting(db, meeting_id)
    if not meeting:
        # Still return pixel even if meeting not found to avoid broken images
        pass
    print(f"Found meeting {meeting_id} for tracking email")
    # Check if user exists
    user = crud.get_user(db, user_id)
    if not user:
        # Still return pixel even if user not found to avoid broken images
        pass
    print(f"Found user {user_id} for tracking email")
    # Check if recipient record exists
    recipient = crud.get_recipient(db, meeting_id, user_id)
    if recipient and recipient.status != "EMAIL_READ":
        # Update status to EMAIL_READ
        crud.update_recipient_status(
            db=db,
            meeting_id=meeting_id,
            user_id=user_id,
            status="EMAIL_READ",
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None
        )
    
    # Return 1x1 transparent pixel image
    # This is a base64 encoded 1x1 transparent PNG
    pixel_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    
    return Response(
        content=pixel_data,
        media_type="image/png",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@router.get("/status/{meeting_id}", response_model=List[schemas.RecipientResponse])
def get_meeting_read_status(meeting_id: int, db: Session = Depends(get_db)):
    """Get read status for all recipients of a meeting"""
    meeting = crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return crud.get_meeting_recipients(db, meeting_id)
