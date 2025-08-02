from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from . import models, schemas
from typing import List, Optional
from datetime import datetime

# User CRUD operations
def get_user(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(models.User).filter(models.User.userId == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get list of users"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Create new user"""
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """Update user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete user"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Meeting CRUD operations
def get_meeting(db: Session, meeting_id: int):
    """Get meeting by ID"""
    return db.query(models.Meeting).filter(models.Meeting.meetingId == meeting_id).first()

def get_meetings(db: Session, skip: int = 0, limit: int = 100):
    """Get list of meetings"""
    return db.query(models.Meeting).offset(skip).limit(limit).all()

def create_meeting(db: Session, meeting: schemas.MeetingCreate):
    """Create new meeting"""
    db_meeting = models.Meeting(title=meeting.title, contentLocation=meeting.contentLocation)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def update_meeting(db: Session, meeting_id: int, meeting_update: schemas.MeetingUpdate):
    """Update meeting"""
    db_meeting = get_meeting(db, meeting_id)
    if not db_meeting:
        return None
    
    update_data = meeting_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meeting, field, value)
    
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def delete_meeting(db: Session, meeting_id: int):
    """Delete meeting"""
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        db.delete(db_meeting)
        db.commit()
    return db_meeting

# Sender CRUD operations
def get_sender(db: Session, meeting_id: int, user_id: int):
    """Get sender by meeting and user ID"""
    return db.query(models.Sender).filter(
        models.Sender.meetingId == meeting_id,
        models.Sender.userId == user_id
    ).first()

def get_meeting_senders(db: Session, meeting_id: int):
    """Get all senders for a meeting"""
    return db.query(models.Sender).filter(models.Sender.meetingId == meeting_id).all()

def create_sender(db: Session, sender: schemas.SenderCreate):
    """Create new sender"""
    # Check if sender already exists
    existing_sender = get_sender(db, sender.meetingId, sender.userId)
    if existing_sender:
        return existing_sender
    
    db_sender = models.Sender(meetingId=sender.meetingId, userId=sender.userId)
    db.add(db_sender)
    db.commit()
    db.refresh(db_sender)
    return db_sender

def delete_sender(db: Session, meeting_id: int, user_id: int):
    """Delete sender"""
    db_sender = get_sender(db, meeting_id, user_id)
    if db_sender:
        db.delete(db_sender)
        db.commit()
    return db_sender

# Recipient CRUD operations
def get_recipient(db: Session, meeting_id: int, user_id: int):
    """Get recipient by meeting and user ID"""
    return db.query(models.Recipient).filter(
        models.Recipient.meetingId == meeting_id,
        models.Recipient.userId == user_id
    ).first()

def get_meeting_recipients(db: Session, meeting_id: int):
    """Get all recipients for a meeting"""
    return db.query(models.Recipient).filter(models.Recipient.meetingId == meeting_id).all()

def get_user_recipients(db: Session, user_id: int):
    """Get all recipient records for a user"""
    return db.query(models.Recipient).filter(models.Recipient.userId == user_id).all()

def create_recipient(db: Session, recipient: schemas.RecipientCreate):
    """Create new recipient"""
    # Check if recipient already exists
    existing_recipient = get_recipient(db, recipient.meetingId, recipient.userId)
    if existing_recipient:
        return existing_recipient
    
    db_recipient = models.Recipient(
        meetingId=recipient.meetingId, 
        userId=recipient.userId,
        status="EMAIL_CREATED"
    )
    db.add(db_recipient)
    db.commit()
    db.refresh(db_recipient)
    return db_recipient

def update_recipient_status(db: Session, meeting_id: int, user_id: int, 
                          status: str, user_agent: str = None, ip_address: str = None):
    """Update recipient status"""
    db_recipient = get_recipient(db, meeting_id, user_id)
    if not db_recipient:
        return None
    
    db_recipient.status = status
    if status == "EMAIL_READ" and db_recipient.read_at is None:
        db_recipient.read_at = func.now()
        db_recipient.user_agent = user_agent
        db_recipient.ip_address = ip_address
    
    db.commit()
    db.refresh(db_recipient)
    return db_recipient

def delete_recipient(db: Session, meeting_id: int, user_id: int):
    """Delete recipient"""
    db_recipient = get_recipient(db, meeting_id, user_id)
    if db_recipient:
        db.delete(db_recipient)
        db.commit()
    return db_recipient

# Analytics operations
def get_meeting_analytics(db: Session, meeting_id: int):
    """Get analytics for a specific meeting"""
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        return None
    
    recipients = get_meeting_recipients(db, meeting_id)
    total_recipients = len(recipients)
    
    email_created_count = len([r for r in recipients if r.status == "EMAIL_CREATED"])
    email_sent_count = len([r for r in recipients if r.status == "EMAIL_SENT"])
    email_read_count = len([r for r in recipients if r.status == "EMAIL_READ"])
    
    read_percentage = (email_read_count / total_recipients * 100) if total_recipients > 0 else 0
    
    return schemas.MeetingAnalytics(
        meetingId=meeting_id,
        meeting_title=meeting.title,
        total_recipients=total_recipients,
        email_created_count=email_created_count,
        email_sent_count=email_sent_count,
        email_read_count=email_read_count,
        read_percentage=round(read_percentage, 2)
    )

def get_user_analytics(db: Session, user_id: int):
    """Get analytics for a specific user"""
    user = get_user(db, user_id)
    if not user:
        return None
    
    recipients = get_user_recipients(db, user_id)
    total_meetings_received = len(recipients)
    total_meetings_read = len([r for r in recipients if r.status == "EMAIL_READ"])
    
    read_percentage = (total_meetings_read / total_meetings_received * 100) if total_meetings_received > 0 else 0
    
    return schemas.UserAnalytics(
        userId=user_id,
        user_name=user.name,
        user_email=user.email,
        total_meetings_received=total_meetings_received,
        total_meetings_read=total_meetings_read,
        read_percentage=round(read_percentage, 2)
    )

def get_overview_analytics(db: Session):
    """Get overview analytics"""
    total_meetings = db.query(models.Meeting).count()
    total_users = db.query(models.User).count()
    total_recipients = db.query(models.Recipient).count()
    total_reads = db.query(models.Recipient).filter(models.Recipient.status == "EMAIL_READ").count()
    
    overall_read_percentage = (total_reads / total_recipients * 100) if total_recipients > 0 else 0
    
    return schemas.OverviewAnalytics(
        total_meetings=total_meetings,
        total_users=total_users,
        total_recipients=total_recipients,
        total_reads=total_reads,
        overall_read_percentage=round(overall_read_percentage, 2)
    )
