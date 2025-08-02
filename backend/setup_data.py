#!/usr/bin/env python3
"""
Setup script to populate the Email Read Tracking database with sample data.
This script uses the FastAPI endpoints to create realistic test data.
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def create_users():
    """Create 10 sample users"""
    users = [
        {"name": "John Doe", "email": "john.doe@company.com"},
        {"name": "Jane Smith", "email": "jane.smith@company.com"},
        {"name": "Michael Johnson", "email": "michael.johnson@company.com"},
        {"name": "Emily Davis", "email": "emily.davis@company.com"},
        {"name": "Robert Wilson", "email": "robert.wilson@company.com"},
        {"name": "Sarah Brown", "email": "sarah.brown@company.com"},
        {"name": "David Lee", "email": "david.lee@company.com"},
        {"name": "Lisa Anderson", "email": "lisa.anderson@company.com"},
        {"name": "James Taylor", "email": "james.taylor@company.com"},
        {"name": "Jennifer Martinez", "email": "jennifer.martinez@company.com"}
    ]
    
    created_users = []
    for user in users:
        response = requests.post(f"{BASE_URL}/users/", json=user)
        if response.status_code == 200:
            created_user = response.json()
            print(f"✓ Created user: {created_user['name']} (ID: {created_user['userId']})")
            created_users.append(created_user)
        else:
            print(f"✗ Failed to create user {user['name']}: {response.text}")
    
    return created_users

def create_meetings():
    """Create 4 sample meetings"""
    meetings = [
        {"title": "Q3 Strategy Planning", "contentLocation": "https://company.com/meetings/q3-strategy"},
        {"title": "Weekly Team Standup", "contentLocation": "https://company.com/meetings/weekly-standup"},
        {"title": "Product Launch Review", "contentLocation": "https://company.com/meetings/product-launch"},
        {"title": "Budget Review Meeting", "contentLocation": "https://company.com/meetings/budget-review"}
    ]
    
    created_meetings = []
    for meeting in meetings:
        response = requests.post(f"{BASE_URL}/meetings/", json=meeting)
        if response.status_code == 200:
            created_meeting = response.json()
            print(f"✓ Created meeting: {created_meeting['title']} (ID: {created_meeting['meetingId']})")
            created_meetings.append(created_meeting)
        else:
            print(f"✗ Failed to create meeting {meeting['title']}: {response.text}")
    
    return created_meetings

def create_senders(meetings, users):
    """Create 1 sender for each meeting"""
    # Assign different users as senders
    sender_assignments = [
        {"meetingId": meetings[0]["meetingId"], "userId": users[0]["userId"]},  # John Doe
        {"meetingId": meetings[1]["meetingId"], "userId": users[2]["userId"]},  # Michael Johnson
        {"meetingId": meetings[2]["meetingId"], "userId": users[4]["userId"]},  # Robert Wilson
        {"meetingId": meetings[3]["meetingId"], "userId": users[7]["userId"]},  # Lisa Anderson
    ]
    
    for sender in sender_assignments:
        response = requests.post(f"{BASE_URL}/senders/", json=sender)
        if response.status_code == 200:
            print(f"✓ Added sender: User {sender['userId']} for Meeting {sender['meetingId']}")
        else:
            print(f"✗ Failed to add sender: {response.text}")

def create_recipients(meetings, users):
    """Create recipients for each meeting with varying numbers"""
    
    # Meeting 1: 7 recipients (users 2,4,6,7,8,9,10)
    meeting1_recipients = [2, 4, 6, 7, 8, 9, 10]
    for user_idx in meeting1_recipients:
        recipient = {"meetingId": meetings[0]["meetingId"], "userId": users[user_idx-1]["userId"]}
        response = requests.post(f"{BASE_URL}/recipients/", json=recipient)
        if response.status_code == 200:
            print(f"✓ Added recipient: User {recipient['userId']} to Meeting {recipient['meetingId']}")
    
    # Meeting 2: 5 recipients (users 1,5,7,9,10)
    meeting2_recipients = [1, 5, 7, 9, 10]
    for user_idx in meeting2_recipients:
        recipient = {"meetingId": meetings[1]["meetingId"], "userId": users[user_idx-1]["userId"]}
        response = requests.post(f"{BASE_URL}/recipients/", json=recipient)
        if response.status_code == 200:
            print(f"✓ Added recipient: User {recipient['userId']} to Meeting {recipient['meetingId']}")
    
    # Meeting 3: 8 recipients (users 1,2,4,6,7,8,9,10)
    meeting3_recipients = [1, 2, 4, 6, 7, 8, 9, 10]
    for user_idx in meeting3_recipients:
        recipient = {"meetingId": meetings[2]["meetingId"], "userId": users[user_idx-1]["userId"]}
        response = requests.post(f"{BASE_URL}/recipients/", json=recipient)
        if response.status_code == 200:
            print(f"✓ Added recipient: User {recipient['userId']} to Meeting {recipient['meetingId']}")
    
    # Meeting 4: 6 recipients (users 1,2,3,5,7,9)
    meeting4_recipients = [1, 2, 3, 5, 7, 9]
    for user_idx in meeting4_recipients:
        recipient = {"meetingId": meetings[3]["meetingId"], "userId": users[user_idx-1]["userId"]}
        response = requests.post(f"{BASE_URL}/recipients/", json=recipient)
        if response.status_code == 200:
            print(f"✓ Added recipient: User {recipient['userId']} to Meeting {recipient['meetingId']}")

def simulate_email_reads(meetings, users):
    """Simulate some email reads by calling the tracking endpoint"""
    
    # Simulate reads for Meeting 1
    reads_meeting1 = [
        (meetings[0]["meetingId"], users[1]["userId"]),  # Jane Smith
        (meetings[0]["meetingId"], users[3]["userId"]),  # Emily Davis
        (meetings[0]["meetingId"], users[6]["userId"]),  # David Lee
        (meetings[0]["meetingId"], users[8]["userId"]),  # James Taylor
    ]
    
    # Simulate reads for Meeting 2
    reads_meeting2 = [
        (meetings[1]["meetingId"], users[0]["userId"]),  # John Doe
        (meetings[1]["meetingId"], users[4]["userId"]),  # Robert Wilson
        (meetings[1]["meetingId"], users[8]["userId"]),  # James Taylor
    ]
    
    # Simulate reads for Meeting 3
    reads_meeting3 = [
        (meetings[2]["meetingId"], users[0]["userId"]),  # John Doe
        (meetings[2]["meetingId"], users[1]["userId"]),  # Jane Smith
        (meetings[2]["meetingId"], users[5]["userId"]),  # Sarah Brown
        (meetings[2]["meetingId"], users[6]["userId"]),  # David Lee
        (meetings[2]["meetingId"], users[8]["userId"]),  # James Taylor
    ]
    
    # Simulate reads for Meeting 4
    reads_meeting4 = [
        (meetings[3]["meetingId"], users[0]["userId"]),  # John Doe
        (meetings[3]["meetingId"], users[2]["userId"]),  # Michael Johnson
        (meetings[3]["meetingId"], users[4]["userId"]),  # Robert Wilson
    ]
    
    all_reads = reads_meeting1 + reads_meeting2 + reads_meeting3 + reads_meeting4
    
    for meeting_id, user_id in all_reads:
        response = requests.get(f"{BASE_URL}/track/email/{meeting_id}/{user_id}")
        if response.status_code == 200:
            print(f"✓ Simulated email read: User {user_id} opened Meeting {meeting_id}")
        else:
            print(f"✗ Failed to simulate read for User {user_id}, Meeting {meeting_id}")

def main():
    """Main setup function"""
    print("🚀 Setting up Email Read Tracking database with sample data...")
    print()
    
    # Check if API is accessible
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API is not accessible. Make sure the FastAPI server is running on port 8000.")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the FastAPI server is running on port 8000.")
        return
    
    print("✓ API is accessible")
    print()
    
    # Create users
    print("👥 Creating users...")
    users = create_users()
    print(f"Created {len(users)} users")
    print()
    
    # Create meetings
    print("📅 Creating meetings...")
    meetings = create_meetings()
    print(f"Created {len(meetings)} meetings")
    print()
    
    # Create senders
    print("📤 Creating senders...")
    create_senders(meetings, users)
    print("Senders created")
    print()
    
    # Create recipients
    print("📥 Creating recipients...")
    create_recipients(meetings, users)
    print("Recipients created")
    print()
    
    # Simulate email reads
    print("📧 Simulating email reads...")
    simulate_email_reads(meetings, users)
    print("Email reads simulated")
    print()
    
    print("✅ Database setup complete!")
    print()
    print("📊 You can now check the analytics:")
    print(f"   - Overview: {BASE_URL}/analytics/overview")
    print(f"   - Meeting analytics: {BASE_URL}/analytics/meeting/1")
    print(f"   - User analytics: {BASE_URL}/analytics/user/1")
    print()
    print("🔍 You can also view the API documentation:")
    print(f"   - Interactive docs: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
