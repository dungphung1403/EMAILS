from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(tags=["senders and recipients"])

# Sender endpoints
@router.post("/senders/", response_model=schemas.SenderResponse)
def create_sender(sender: schemas.SenderCreate, db: Session = Depends(get_db)):
    """Add a sender to a meeting"""
    # Verify meeting exists
    meeting = crud.get_meeting(db, sender.meetingId)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Verify user exists
    user = crud.get_user(db, sender.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.create_sender(db=db, sender=sender)

@router.delete("/senders/{meeting_id}/{user_id}")
def delete_sender(meeting_id: int, user_id: int, db: Session = Depends(get_db)):
    """Remove a sender from a meeting"""
    db_sender = crud.delete_sender(db, meeting_id=meeting_id, user_id=user_id)
    if db_sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")
    return {"message": "Sender removed successfully"}

# Recipient endpoints
@router.post("/recipients/", response_model=schemas.RecipientResponse)
def create_recipient(recipient: schemas.RecipientCreate, db: Session = Depends(get_db)):
    """Add a recipient to a meeting"""
    # Verify meeting exists
    meeting = crud.get_meeting(db, recipient.meetingId)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Verify user exists
    user = crud.get_user(db, recipient.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.create_recipient(db=db, recipient=recipient)

@router.put("/recipients/{meeting_id}/{user_id}", response_model=schemas.RecipientResponse)
def update_recipient_status(
    meeting_id: int, 
    user_id: int, 
    recipient_update: schemas.RecipientUpdate, 
    db: Session = Depends(get_db)
):
    """Update recipient status"""
    if recipient_update.status:
        db_recipient = crud.update_recipient_status(
            db, 
            meeting_id=meeting_id, 
            user_id=user_id, 
            status=recipient_update.status.value
        )
        if db_recipient is None:
            raise HTTPException(status_code=404, detail="Recipient not found")
        return db_recipient
    else:
        raise HTTPException(status_code=400, detail="Status is required")

@router.delete("/recipients/{meeting_id}/{user_id}")
def delete_recipient(meeting_id: int, user_id: int, db: Session = Depends(get_db)):
    """Remove a recipient from a meeting"""
    db_recipient = crud.delete_recipient(db, meeting_id=meeting_id, user_id=user_id)
    if db_recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return {"message": "Recipient removed successfully"}
