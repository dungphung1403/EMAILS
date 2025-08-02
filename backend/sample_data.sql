-- Sample Data Setup for Email Read Tracking Database
-- This script populates all 4 tables with realistic test data

-- Insert 10 Users
INSERT INTO user (userId, name, email, created_at, updated_at) VALUES
(1, 'John Doe', 'john.doe@company.com', '2025-07-15 09:00:00', '2025-07-15 09:00:00'),
(2, 'Jane Smith', 'jane.smith@company.com', '2025-07-16 10:30:00', '2025-07-16 10:30:00'),
(3, 'Michael Johnson', 'michael.johnson@company.com', '2025-07-17 11:15:00', '2025-07-17 11:15:00'),
(4, 'Emily Davis', 'emily.davis@company.com', '2025-07-18 14:20:00', '2025-07-18 14:20:00'),
(5, 'Robert Wilson', 'robert.wilson@company.com', '2025-07-19 16:45:00', '2025-07-19 16:45:00'),
(6, 'Sarah Brown', 'sarah.brown@company.com', '2025-07-20 08:30:00', '2025-07-20 08:30:00'),
(7, 'David Lee', 'david.lee@company.com', '2025-07-21 13:10:00', '2025-07-21 13:10:00'),
(8, 'Lisa Anderson', 'lisa.anderson@company.com', '2025-07-22 15:25:00', '2025-07-22 15:25:00'),
(9, 'James Taylor', 'james.taylor@company.com', '2025-07-23 09:50:00', '2025-07-23 09:50:00'),
(10, 'Jennifer Martinez', 'jennifer.martinez@company.com', '2025-07-24 12:40:00', '2025-07-24 12:40:00');

-- Insert 4 Meetings
INSERT INTO meeting (meetingId, title, contentLocation, created_at, updated_at) VALUES
(1, 'Q3 Strategy Planning', 'https://company.com/meetings/q3-strategy', '2025-07-25 09:00:00', '2025-07-25 09:00:00'),
(2, 'Weekly Team Standup', 'https://company.com/meetings/weekly-standup', '2025-07-26 14:30:00', '2025-07-26 14:30:00'),
(3, 'Product Launch Review', 'https://company.com/meetings/product-launch', '2025-07-27 10:15:00', '2025-07-27 10:15:00'),
(4, 'Budget Review Meeting', 'https://company.com/meetings/budget-review', '2025-07-28 16:00:00', '2025-07-28 16:00:00');

-- Insert 1 Sender for each meeting
INSERT INTO sender (meetingId, userId, created_at) VALUES
(1, 1, '2025-07-25 09:15:00'),  -- John Doe sends Q3 Strategy Planning
(2, 3, '2025-07-26 14:45:00'),  -- Michael Johnson sends Weekly Team Standup
(3, 5, '2025-07-27 10:30:00'),  -- Robert Wilson sends Product Launch Review
(4, 8, '2025-07-28 16:15:00');  -- Lisa Anderson sends Budget Review Meeting

-- Insert Recipients for Meeting 1 (Q3 Strategy Planning) - 7 recipients
INSERT INTO recipient (meetingId, userId, status, read_at, user_agent, ip_address, created_at, updated_at) VALUES
(1, 2, 'EMAIL_READ', '2025-07-25 11:30:00', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.101', '2025-07-25 09:20:00', '2025-07-25 11:30:00'),
(1, 4, 'EMAIL_READ', '2025-07-25 13:45:00', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.102', '2025-07-25 09:20:00', '2025-07-25 13:45:00'),
(1, 6, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-25 09:20:00', '2025-07-25 09:45:00'),
(1, 7, 'EMAIL_READ', '2025-07-25 15:20:00', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.103', '2025-07-25 09:20:00', '2025-07-25 15:20:00'),
(1, 8, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-25 09:20:00', '2025-07-25 09:45:00'),
(1, 9, 'EMAIL_READ', '2025-07-25 17:10:00', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0', '192.168.1.104', '2025-07-25 09:20:00', '2025-07-25 17:10:00'),
(1, 10, 'EMAIL_CREATED', NULL, NULL, NULL, '2025-07-25 09:20:00', '2025-07-25 09:20:00');

-- Insert Recipients for Meeting 2 (Weekly Team Standup) - 5 recipients
INSERT INTO recipient (meetingId, userId, status, read_at, user_agent, ip_address, created_at, updated_at) VALUES
(2, 1, 'EMAIL_READ', '2025-07-26 15:30:00', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.105', '2025-07-26 14:50:00', '2025-07-26 15:30:00'),
(2, 5, 'EMAIL_READ', '2025-07-26 16:45:00', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15', '192.168.1.106', '2025-07-26 14:50:00', '2025-07-26 16:45:00'),
(2, 7, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-26 14:50:00', '2025-07-26 15:15:00'),
(2, 9, 'EMAIL_READ', '2025-07-26 18:20:00', 'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/115.0', '192.168.1.107', '2025-07-26 14:50:00', '2025-07-26 18:20:00'),
(2, 10, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-26 14:50:00', '2025-07-26 15:15:00');

-- Insert Recipients for Meeting 3 (Product Launch Review) - 8 recipients
INSERT INTO recipient (meetingId, userId, status, read_at, user_agent, ip_address, created_at, updated_at) VALUES
(3, 1, 'EMAIL_READ', '2025-07-27 12:15:00', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.108', '2025-07-27 10:45:00', '2025-07-27 12:15:00'),
(3, 2, 'EMAIL_READ', '2025-07-27 13:30:00', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.109', '2025-07-27 10:45:00', '2025-07-27 13:30:00'),
(3, 4, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-27 10:45:00', '2025-07-27 11:10:00'),
(3, 6, 'EMAIL_READ', '2025-07-27 14:45:00', 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.110', '2025-07-27 10:45:00', '2025-07-27 14:45:00'),
(3, 7, 'EMAIL_READ', '2025-07-27 16:20:00', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.111', '2025-07-27 10:45:00', '2025-07-27 16:20:00'),
(3, 8, 'EMAIL_CREATED', NULL, NULL, NULL, '2025-07-27 10:45:00', '2025-07-27 10:45:00'),
(3, 9, 'EMAIL_READ', '2025-07-27 17:50:00', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0', '192.168.1.112', '2025-07-27 10:45:00', '2025-07-27 17:50:00'),
(3, 10, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-27 10:45:00', '2025-07-27 11:10:00');

-- Insert Recipients for Meeting 4 (Budget Review Meeting) - 6 recipients
INSERT INTO recipient (meetingId, userId, status, read_at, user_agent, ip_address, created_at, updated_at) VALUES
(4, 1, 'EMAIL_READ', '2025-07-28 17:30:00', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.113', '2025-07-28 16:30:00', '2025-07-28 17:30:00'),
(4, 2, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-28 16:30:00', '2025-07-28 16:55:00'),
(4, 3, 'EMAIL_READ', '2025-07-28 19:15:00', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15', '192.168.1.114', '2025-07-28 16:30:00', '2025-07-28 19:15:00'),
(4, 5, 'EMAIL_READ', '2025-07-28 20:45:00', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.115', '2025-07-28 16:30:00', '2025-07-28 20:45:00'),
(4, 7, 'EMAIL_CREATED', NULL, NULL, NULL, '2025-07-28 16:30:00', '2025-07-28 16:30:00'),
(4, 9, 'EMAIL_SENT', NULL, NULL, NULL, '2025-07-28 16:30:00', '2025-07-28 16:55:00');

-- Summary of the data:
-- - 10 users with realistic names and company emails
-- - 4 meetings with different purposes and content locations
-- - 1 sender per meeting (different users)
-- - Meeting 1: 7 recipients (4 read, 2 sent, 1 created)
-- - Meeting 2: 5 recipients (3 read, 2 sent)
-- - Meeting 3: 8 recipients (5 read, 2 sent, 1 created)
-- - Meeting 4: 6 recipients (3 read, 2 sent, 1 created)
-- - Total: 26 recipient records with various statuses
-- - Realistic timestamps showing email progression over time
-- - Different user agents representing various devices/browsers
-- - IP addresses for tracking purposes
