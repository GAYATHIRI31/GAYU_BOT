import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- Email Config ---
FROM_EMAIL = "gayathirik31@gmail.com"
TO_EMAIL = "gayathiri3132000@gmail.com"
APP_PASSWORD = "your_gmail_app_password"

NO_RESPONSES = [
    "I understand... but my heart says otherwise. Can I ask you one more time? ❤️",
    "I respect your answer, but feelings this strong don't come easy. Won't you give us a chance? 🙏",
    "Okay, I hear you. But just so you know — I'll still be here for her, always. Maybe someday? 🌟",
    "Your happiness matters most to her. Even as a friend, she'll always care for you. 💙",
]

# --- Send Email ---
def send_email(chat_history):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "💌 Proposal Response Received!"
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL

        plain_text = f"Proposal Response - {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\n"
        plain_text += "=" * 40 + "\n\n"
        for role, text in chat_history:
            label = "GAYU's Bot" if role == "bot" else "They"
            plain_text += f"{label}:\n{text}\n\n"

        html_rows = ""
        for role, text in chat_history:
            if role == "bot":
                html_rows += f"""
                <tr>
                  <td style="padding:8px 12px; background:#FBEAF0; color:#4B1528;
                             border-radius:12px; margin:4px 0; display:block;
                             max-width:80%; font-size:14px;">
                    <strong>💬 Bot:</strong> {text}
                  </td>
                </tr>"""
            else:
                html_rows += f"""
                <tr>
                  <td style="padding:8px 12px; background:#D4537E; color:white;
                             border-radius:12px; margin:4px 0; display:block;
                             max-width:80%; text-align:right; font-size:14px;">
                    <strong>💕 They:</strong> {text}
                  </td>
                </tr>"""

        html = f"""
        <html><body style="font-family:Arial,sans-serif; padding:20px;">
          <h2 style="color:#993556;">💌 Proposal Response Received!</h2>
          <p style="color:gray;">on {datetime.now().strftime('%d %b %Y at %I:%M %p')}</p>
          <hr style="border:0.5px solid #f4c0d1; margin:16px 0;">
          <table style="width:100%; border-collapse:separate; border-spacing:0 6px;">
            {html_rows}
          </table>
          <hr style="border:0.5px solid #f4c0d1; margin:16px 0;">
          <p style="color:#993556; font-size:13px;">Sent with ❤️ from GAYU's Proposal Bot</p>
        </body></html>
        """

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False

# --- UI ---
st.set_page_config(page_title="A Message for You", page_icon="❤️")

st.markdown("""
<style>
.bot-msg {
    background:#FBEAF0; color:#4B1528;
    padding:10px 16px; border-radius:18px 18px 18px 4px;
    margin:6px 0; max-width:80%; font-size:15px; line-height:1.6;
}
.user-msg {
    background:#D4537E; color:white;
    padding:10px 16px; border-radius:18px 18px 4px 18px;
    margin:6px 0 6px auto; max-width:80%;
    font-size:15px; text-align:right;
}
.fireworks {
    text-align:center; padding:2rem;
    font-size:20px; color:#993556;
    background:#FBEAF0; border-radius:16px; margin-top:1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center'>❤️ A Message for You</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>From someone who cares about you deeply</p>", unsafe_allow_html=True)
st.divider()

# --- Session State ---
if "step" not in st.session_state:
    st.session_state.step = "start"
if "messages" not in st.session_state:
    st.session_state.messages = [
        ("bot", "Hi there 👋 I hope you're doing well today!"),
        ("bot", "Someone very special asked me to pass along a message for you..."),
        ("bot", "Her name is GAYU, and she has something important to say. Are you ready to hear it? ❤️"),
    ]
if "no_count" not in st.session_state:
    st.session_state.no_count = 0
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# --- Display Messages ---
for role, text in st.session_state.messages:
    if role == "bot":
        st.markdown(f"<div class='bot-msg'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='user-msg'>{text}</div>", unsafe_allow_html=True)

# --- Send email once when conversation ends ---
def finish(final_bot_msg):
    st.session_state.messages.append(("bot", final_bot_msg))
    st.session_state.step = "done"
    if not st.session_state.email_sent:
        if send_email(st.session_state.messages):
            st.session_state.email_sent = True
    st.rerun()

# --- Steps ---
if st.session_state.step == "yes":
    st.markdown("""
    <div class='fireworks'>
        🎉❤️🎊<br><br>
        <strong>You said YES!</strong> 😍<br><br>
        GAYU's heart is overflowing with joy right now.<br>
        This is just the beginning of something beautiful. ✨
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.email_sent:
        if send_email(st.session_state.messages):
            st.session_state.email_sent = True

elif st.session_state.step == "done":
    st.info("Thank you for your response. 💙")

elif st.session_state.step == "start":
    col1, col2 = st.columns(2)
    if col1.button("Yes, I'm ready! 🙌"):
        st.session_state.messages.append(("user", "Yes, I'm ready!"))
        st.session_state.messages.append(("bot", "💌 Ever since she met you, her world has felt brighter. Your smile, your kindness — everything about you makes her heart feel at home. Today she finally wants to say it..."))
        st.session_state.messages.append(("bot", "✨ Will you be her love? ✨"))
        st.session_state.step = "proposal"
        st.rerun()
    if col2.button("Hmm, okay..."):
        st.session_state.messages.append(("user", "Hmm, okay..."))
        st.session_state.messages.append(("bot", "💌 Ever since she met you, her world has felt brighter. Your smile, your kindness — everything about you makes her heart feel at home. Today she finally wants to say it..."))
        st.session_state.messages.append(("bot", "✨ Will you be her love? ✨"))
        st.session_state.step = "proposal"
        st.rerun()

elif st.session_state.step == "proposal":
    col1, col2, col3 = st.columns(3)
    if col1.button("❤️ Yes!"):
        st.session_state.messages.append(("user", "Yes! ❤️"))
        st.session_state.messages.append(("bot", "🎉 Oh my goodness! GAYU is the happiest person alive right now! You just made her heart do a thousand somersaults. 😍"))
        st.session_state.step = "yes"
        st.rerun()
    if col2.button("I need to think..."):
        st.session_state.messages.append(("user", "I need to think..."))
        st.session_state.messages.append(("bot", "That's completely okay. 😊 GAYU understands — feelings need time. She will wait, no pressure at all. 💙"))
        st.session_state.step = "maybe"
        st.rerun()
    if col3.button("No"):
        st.session_state.messages.append(("user", "No"))
        st.session_state.messages.append(("bot", NO_RESPONSES[0]))
        st.session_state.no_count = 1
        st.session_state.step = "no"
        st.rerun()

elif st.session_state.step == "maybe":
    col1, col2, col3 = st.columns(3)
    if col1.button("❤️ Actually, Yes!"):
        st.session_state.messages.append(("user", "Actually, Yes! ❤️"))
        st.session_state.messages.append(("bot", "🎉 GAYU is over the moon! 😍 Thank you for giving love a chance!"))
        st.session_state.step = "yes"
        st.rerun()
    if col2.button("Maybe later"):
        finish("That means the world to her. 🌟 GAYU will be right here, whenever you are ready.")
    if col3.button("No"):
        st.session_state.messages.append(("user", "No"))
        st.session_state.messages.append(("bot", NO_RESPONSES[0]))
        st.session_state.no_count = 1
        st.session_state.step = "no"
        st.rerun()

elif st.session_state.step == "no":
    col1, col2 = st.columns(2)
    if col1.button("❤️ Okay, Yes!"):
        st.session_state.messages.append(("user", "Okay, Yes! ❤️"))
        st.session_state.messages.append(("bot", "🎉 GAYU is OVER THE MOON right now! 😍"))
        st.session_state.step = "yes"
        st.rerun()
    if col2.button("Still no"):
        nc = st.session_state.no_count
        if nc < len(NO_RESPONSES):
            st.session_state.messages.append(("user", "No"))
            st.session_state.messages.append(("bot", NO_RESPONSES[nc]))
            st.session_state.no_count += 1
            st.rerun()
        else:
            finish("GAYU respects your decision. She wishes you all the happiness in the world. 💙")
