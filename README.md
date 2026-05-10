# GAYU_BOT
Alright Gayu, let’s walk through your code step by step so you understand exactly what’s happening and why you saw those errors earlier. I’ll explain the **structure, purpose, and flow** of your app:

---

## 1. Imports and Setup
```python
import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo   # for correct IST time
```
- **streamlit** → builds the interactive web app.
- **requests** → sends HTTP requests to Telegram’s API.
- **datetime** → gets current date/time.
- **ZoneInfo** → ensures you use the correct timezone (Asia/Kolkata).

---

## 2. Telegram Config
```python
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
```
- You store your bot token and chat ID securely in Streamlit secrets.
- These are used to send messages to your Telegram account.

---

## 3. Predefined “No” Responses
```python
NO_RESPONSES = [
    "I understand... but my heart says otherwise. Can I ask you one more time? 💙",
    ...
]
```
- A list of polite fallback messages when the user clicks “No”.

---

## 4. Sending Telegram Messages
```python
def send_telegram(chat_history_or_text):
    ...
```
- This function handles sending messages to Telegram.
- It accepts either:
  - A **list of chat history** (bot + user messages).
  - A **single text string**.
- It formats the message and posts it to Telegram using `requests.post`.

---

## 5. Entry Notification
```python
current_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y, %I:%M %p")
send_telegram(f"📥 He is inside the chat now - {current_time}")
```
- Every time the app loads, it sends a Telegram message saying the person entered the chat.
- The time is formatted in **IST** so you see the correct local time.

---

## 6. UI Styling
```python
st.set_page_config(page_title="A Message for You", page_icon="💙")
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
```
- Sets the page title and icon.
- Defines CSS styles for bot messages, user messages, and fireworks.

---

## 7. Exit Notification
```python
st.markdown("""
<script>
window.addEventListener("beforeunload", function (e) {
    navigator.sendBeacon("/?out=1");
});
</script>
""", unsafe_allow_html=True)

query_params = st.query_params
if "out" in query_params:
    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y, %I:%M %p")
    send_telegram(f"📤 He is out of chat now - {current_time}")
    st.stop()
```
- Injects JavaScript that pings the server when the tab closes.
- If `out=1` is detected in the URL, it sends a Telegram message saying the person left, with the correct IST time.

---

## 8. Session State
```python
if "step" not in st.session_state:
    st.session_state.step = "start"
...
```
- Keeps track of where the user is in the conversation (`start`, `proposal`, `yes`, `no`, etc.).
- Stores chat messages and counts how many times “No” was clicked.

---

## 9. Display Messages
```python
for role, text in st.session_state.messages:
    if role == "bot":
        st.markdown(f"<div class='bot-msg'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='user-msg'>{text}</div>", unsafe_allow_html=True)
```
- Shows messages in styled chat bubbles.

---

## 10. Conversation Flow
- **start step** → shows “Yes, I’m ready!” and “Hmm, okay...” buttons.
- **proposal step** → shows “Yes!”, “I need to think...”, “No”.
- **maybe step** → shows “Actually Yes!”, “Maybe later”, “No”.
- **no step** → cycles through polite refusal messages until final respect message.
- **yes step** → shows fireworks celebration.

Each button click:
- Adds a message to chat history.
- Sends the updated chat to Telegram.
- Updates `st.session_state.step`.
- Calls `st.rerun()` to refresh the app.

---

## 🔑 Key Fixes You Needed
1. **Timezone mismatch** → solved by `ZoneInfo("Asia/Kolkata")`.
2. **Deprecated API** → replaced `st.experimental_get_query_params()` with `st.query_params`.
3. **Indentation error** → removed stray spaces and lines in the `proposal` step.

---

## 🎯 What You Achieved
- A romantic interactive proposal app.
- Every user action is logged to Telegram.
- You now also get **entry and exit notifications with correct IST time**.

---

Would you like me to **regenerate the full file** with all these fixes applied (IST time, correct query params, clean indentation), so you can copy‑paste it directly without worrying about missing pieces?
