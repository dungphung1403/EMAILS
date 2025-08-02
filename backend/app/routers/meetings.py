from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/meetings", tags=["meetings"])

@router.post("/", response_model=schemas.MeetingResponse)
def create_meeting(meeting: schemas.MeetingCreate, db: Session = Depends(get_db)):
    """Create a new meeting"""
    return crud.create_meeting(db=db, meeting=meeting)

@router.get("/", response_model=List[schemas.MeetingResponse])
def list_meetings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all meetings"""
    return crud.get_meetings(db, skip=skip, limit=limit)

@router.get("/{meeting_id}", response_model=schemas.MeetingResponse)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """Get a specific meeting by ID"""
    db_meeting = crud.get_meeting(db, meeting_id=meeting_id)
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return db_meeting

@router.put("/{meeting_id}", response_model=schemas.MeetingResponse)
def update_meeting(
    meeting_id: int, 
    meeting_update: schemas.MeetingUpdate, 
    db: Session = Depends(get_db)
):
    """Update a specific meeting"""
    db_meeting = crud.update_meeting(db, meeting_id=meeting_id, meeting_update=meeting_update)
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return db_meeting

@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """Delete a specific meeting"""
    db_meeting = crud.delete_meeting(db, meeting_id=meeting_id)
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"message": "Meeting deleted successfully"}

@router.get("/{meeting_id}/senders", response_model=List[schemas.SenderResponse])
def get_meeting_senders(meeting_id: int, db: Session = Depends(get_db)):
    """Get all senders for a specific meeting"""
    meeting = crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return crud.get_meeting_senders(db, meeting_id)

@router.get("/{meeting_id}/recipients", response_model=List[schemas.RecipientResponse])
def get_meeting_recipients(meeting_id: int, db: Session = Depends(get_db)):
    """Get all recipients for a specific meeting"""
    meeting = crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return crud.get_meeting_recipients(db, meeting_id)
