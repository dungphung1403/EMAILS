
import json
import os
import streamlit as st
from azure.communication.email import EmailClient
from db import insert_email
from email_content import summarize_transcript, create_html_email_from_json
from dotenv import load_dotenv


load_dotenv()
email_client = EmailClient.from_connection_string(os.getenv("ACS_CONNECTION_STRING"))

st.set_page_config(page_title="AI Support Email Demo")
st.title("🔔 AI-Powered Support Email Demo")

recipient = st.text_input("Recipient email", value=os.getenv("RECIPIENT_EMAIL"))
# recipient1 = st.text_input("Recipient email 1", value=os.getenv("RECIPIENT_EMAIL1"))
subject   = st.text_input("Email subject", value="MOM - Meeting Summary")
query     = st.file_uploader("Upload a transcript file", type=["txt"])

# 1) GENERATE
if st.button("🧠 Generate Reply"):
    if not query:
        st.error("Enter a customer query first.")
    else:
        with st.spinner("Generating…"):
            summary = summarize_transcript(query)
            summary_dict = json.loads(summary)
            print(summary_dict)
            print(query)
            st.session_state["draft"] = create_html_email_from_json(summary_dict)
            # st.session_state["draft"] = summary

# 2) PREVIEW & EDIT
if "draft" in st.session_state:
    st.markdown("**✏️ Edit your email before sending:**")
    st.session_state["edited"] = st.text_area(
        "Email body", 
        value=st.session_state["draft"], 
        height=300
    )

    # 3) SEND
    if st.button("📤 Send Email"):
        msg = {
            "senderAddress": os.getenv("ACS_SENDER_EMAIL"),
            "content": {
                "subject": subject,
                "plainText": st.session_state["edited"]
            },
            "recipients": {"to":[{"address": recipient} ]},
        }
        with st.spinner("Sending…"):
            poller = email_client.begin_send(msg)
            result = poller.result()
            pass  # Placeholder to satisfy indentation
        st.success(f"Email sent! ID: {result['id']}")
        st.write("Status:", result.get("status"))
