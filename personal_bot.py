import requests
import streamlit as st
from datetime import datetime

TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

def send_telegram(chat_history):
    try:
        plain_text = f"💌 Proposal Response - {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\n"
        for role, text in chat_history:
            label = "Bot" if role == "bot" else "They"
            plain_text += f"{label}: {text}\n\n"

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": plain_text}
        requests.post(url, data=data)
        return True
    except Exception as e:
        st.error(f"Telegram failed: {e}")
        return False
