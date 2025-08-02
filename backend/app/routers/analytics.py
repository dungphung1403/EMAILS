from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/meeting/{meeting_id}", response_model=schemas.MeetingAnalytics)
def get_meeting_analytics(meeting_id: int, db: Session = Depends(get_db)):
    """Get analytics for a specific meeting"""
    analytics = crud.get_meeting_analytics(db, meeting_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return analytics

@router.get("/user/{user_id}", response_model=schemas.UserAnalytics)
def get_user_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get analytics for a specific user"""
    analytics = crud.get_user_analytics(db, user_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="User not found")
    
    return analytics

@router.get("/overview", response_model=schemas.OverviewAnalytics)
def get_overview_analytics(db: Session = Depends(get_db)):
    """Get overview analytics"""
    return crud.get_overview_analytics(db)
