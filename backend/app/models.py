from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Meeting(Base):
    """Meeting model for storing meeting information"""
    __tablename__ = "meeting"
    
    meetingId = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    contentLocation = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    senders = relationship("Sender", back_populates="meeting")
    recipients = relationship("Recipient", back_populates="meeting")

class User(Base):
    """User model for storing user information"""
    __tablename__ = "user"
    
    userId = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sent_meetings = relationship("Sender", back_populates="user")
    received_meetings = relationship("Recipient", back_populates="user")

class Sender(Base):
    """Sender model for tracking who sent meeting emails"""
    __tablename__ = "sender"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    meetingId = Column(Integer, ForeignKey("meeting.meetingId"), nullable=False)
    userId = Column(Integer, ForeignKey("user.userId"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    meeting = relationship("Meeting", back_populates="senders")
    user = relationship("User", back_populates="sent_meetings")

class Recipient(Base):
    """Recipient model for tracking email recipients and read status"""
    __tablename__ = "recipient"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    meetingId = Column(Integer, ForeignKey("meeting.meetingId"), nullable=False)
    userId = Column(Integer, ForeignKey("user.userId"), nullable=False)
    status = Column(String(50), nullable=False, default="EMAIL_CREATED")
    read_at = Column(DateTime(timezone=True), nullable=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    meeting = relationship("Meeting", back_populates="recipients")
    user = relationship("User", back_populates="received_meetings")
