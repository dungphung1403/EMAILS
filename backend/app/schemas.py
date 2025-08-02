from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Status enum for recipients
class RecipientStatus(str, Enum):
    EMAIL_CREATED = "EMAIL_CREATED"
    EMAIL_SENT = "EMAIL_SENT"
    EMAIL_READ = "EMAIL_READ"

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    userId: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Meeting schemas
class MeetingBase(BaseModel):
    title: str
    contentLocation: Optional[str] = None

class MeetingCreate(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    contentLocation: Optional[str] = None

class MeetingResponse(MeetingBase):
    meetingId: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Sender schemas
class SenderBase(BaseModel):
    meetingId: int
    userId: int

class SenderCreate(SenderBase):
    pass

class SenderResponse(SenderBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Recipient schemas
class RecipientBase(BaseModel):
    meetingId: int
    userId: int

class RecipientCreate(RecipientBase):
    pass

class RecipientUpdate(BaseModel):
    status: Optional[RecipientStatus] = None

class RecipientResponse(RecipientBase):
    id: int
    status: str
    read_at: Optional[datetime] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Analytics schemas
class MeetingAnalytics(BaseModel):
    meetingId: int
    meeting_title: str
    total_recipients: int
    email_created_count: int
    email_sent_count: int
    email_read_count: int
    read_percentage: float

class UserAnalytics(BaseModel):
    userId: int
    user_name: str
    user_email: str
    total_meetings_received: int
    total_meetings_read: int
    read_percentage: float

class OverviewAnalytics(BaseModel):
    total_meetings: int
    total_users: int
    total_recipients: int
    total_reads: int
    overall_read_percentage: float

# Response schemas
class TrackingResponse(BaseModel):
    success: bool
    message: str
    already_read: bool = False
