import os
from openai import AzureOpenAI
import re
from datetime import datetime
from dotenv import load_dotenv

# clients
load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def summarize_transcript(text):
    prompt = (
    'Summarize the following meeting transcript using the structure below:\n'
    '{\n'
    '  "meeting_type": "...",\n'
    '  "meeting_title": "...",\n'
    '  "meeting_date": "...",\n'
    '  "summary": "...",\n'
    '  "action_items": [\n'
    '     {"person": "...", "task": "...", "deadline": "..."}\n'
    '  ],\n'
    '  "recipients": ["...", "..."]\n'
    '}\n\n'
    'Notes:\n'
    '- Extract email addresses mentioned in the transcript and list them under "recipients".\n'
    '- Ensure "meeting_title" and "meeting_date" are inferred if explicitly stated; otherwise, mark them as "Unknown".\n'
    '- Keep the summary concise and highlight key discussion points.\n'
    '- List action items clearly with assigned person, task.\n'
    '- Ensure fill "deadline" follows the task if tasks do not mention about deadline, write "No information" then for "deadline"\n'
    f"Transcript:\n{text}\n"
)
 
    response = client.chat.completions.create(
        model="GPT-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in summarizing meeting notes in a transcript meeting with Multilingual support. Your language response will follow the language in the transcript."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
 

def bold_numbers(text: str) -> str:
    """
    Wraps any number (or percentage) in <strong> tags.
    E.g. 'Revenue grew 25%' -> 'Revenue grew <strong>25%</strong>'
    """
    return re.sub(r'(\d+%?\.?\d*)', r'<strong>\1</strong>', text)
 
def create_html_email_from_json(meeting_data: dict, tracking_url=None) -> str:
    """
    Generate a Gmail/Outlook friendly HTML email from structured meeting JSON.
    Supports an optional tracking pixel.
    """
 
    # Extract fields
    meeting_title = meeting_data.get("meeting_title", "Meeting Summary")
    meeting_date = meeting_data.get("meeting_date", datetime.now().strftime("%B %d, %Y"))
    summary = bold_numbers(meeting_data.get("summary", "No summary provided."))
    action_items = meeting_data.get("action_items", [])
    sender_name = meeting_data.get("sender_name", "Your Name")
    recipients = meeting_data.get("recipients", [])
 
    # Build action items list
    action_items_html = ""
    for item in action_items:
        person = item.get("person", "Someone")
        task = bold_numbers(item.get("task", "No task specified"))
        deadline = bold_numbers(item.get("deadline", "No deadline"))
        action_items_html += f"<li><strong>{person}</strong>: {task} <em>(Due: {deadline})</em></li>"
 
    # Add tracking pixel if provided
    tracking_pixel_html = f'<img src="{tracking_url}" alt="" width="1" height="1" style="display:none;">' if tracking_url else ""
 
    # HTML template (safe for Gmail/Outlook)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; padding: 20px; }}
  h2 {{ color: #2C3E50; }}
  ul {{ padding-left: 20px; }}
  li {{ margin-bottom: 8px; }}
  .footer {{ margin-top: 20px; font-size: 12px; color: #777; }}
</style>
</head>
<body>
<h2>{meeting_title}</h2>
<p><em>Date: {meeting_date}</em></p>
<p>Hi {", ".join(recipients) if recipients else "Team"},</p>
 
  <p>{summary}</p>
 
  <p><strong>Action Items:</strong></p>
<ul>{action_items_html}</ul>
 
  <p>Thanks,<br>{sender_name}</p>
 
  {tracking_pixel_html}
 
  <div class="footer">
<p>This email was auto-generated from meeting data.</p>
</div>
</body>
</html>"""
    return html_content