import streamlit as st
import requests
from datetime import datetime

# --- Telegram Config ---
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

NO_RESPONSES = [
    "I understand... but my heart says otherwise. Can I ask you one more time? 💙",
    "I respect your answer, but feelings this strong don't come easy. Won't you give us a chance? 🙏",
    "Okay, I hear you. But just so you know , I'll still be here for her, always. Maybe someday? 🌟",
    "Your happiness matters most to her. Even as a well wisher, she'll always care for you. 💙",
]

# --- Send Telegram ---
def send_telegram(chat_history_or_text):
    try:
        if isinstance(chat_history_or_text, list):
            plain_text = f"💌 Proposal Response - {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\n"
            for role, text in chat_history_or_text:
                label = "GAYU's Bot" if role == "bot" else "They"
                plain_text += f"{label}: {text}\n\n"
        else:
            plain_text = chat_history_or_text

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": plain_text}
        requests.post(url, data=data)
        return True
    except Exception as e:
        st.error(f"Telegram failed: {e}")
        return False

# --- Notify on entry ---
if "entered" not in st.session_state:
    st.session_state.entered = True
    send_telegram("📥 He is inside the chat now")

# --- UI ---
st.set_page_config(page_title="A Message for You", page_icon="💙")

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

st.markdown("<h2 style='text-align:center'>💙 A Message for You</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>From someone who cares about you deeply</p>", unsafe_allow_html=True)
st.divider()

# --- Notify on exit (tab close) ---
st.markdown("""
<script>
window.addEventListener("beforeunload", function (e) {
    navigator.sendBeacon("/?out=1");  // ping server when tab closes
});
</script>
""", unsafe_allow_html=True)

# --- Handle tab close ping ---
query_params = st.query_params
if "out" in query_params:
    send_telegram("📤 He is out of chat now")
    st.stop()

# --- Session State ---
if "step" not in st.session_state:
    st.session_state.step = "start"
if "messages" not in st.session_state:
    st.session_state.messages = [
        ("bot", "Hi SAKTHI 👋 I hope you're doing well!"),
        ("bot", "Someone very special asked me to pass along a message for you..."),
        ("bot", "Her name is GAYU, and she has something important to say. Are you ready to hear it? 💙"),
    ]
if "no_count" not in st.session_state:
    st.session_state.no_count = 0

# --- Display Messages ---
for role, text in st.session_state.messages:
    if role == "bot":
        st.markdown(f"<div class='bot-msg'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='user-msg'>{text}</div>", unsafe_allow_html=True)

# --- Finish helper ---
def finish(final_bot_msg):
    st.session_state.messages.append(("bot", final_bot_msg))
    st.session_state.step = "done"
    send_telegram(st.session_state.messages)
    st.rerun()

# --- Steps ---
if st.session_state.step == "yes":
    st.markdown("""
    <div class='fireworks'>
        🎉💙💙🎊<br><br>
        <strong>You said YES!</strong> 😍😍<br><br>
        GAYU's heart is overflowing with joy right now.<br>
        This is just the beginning of something beautiful. ✨
    </div>
    """, unsafe_allow_html=True)
    send_telegram(st.session_state.messages)

elif st.session_state.step == "done":
    st.info("Thank you for your response. 💙")

elif st.session_state.step == "start":
    col1, col2 = st.columns(2)
    if col1.button("Yes, I'm ready! 🙌"):
        st.session_state.messages.append(("user", "Yes, I'm ready!"))
        st.session_state.messages.append(("bot", """💌 Ever since I met you, my world has felt brighter. 
Your smile, your presence, and everything about you makes my heart feel at home. 
I want that feeling forever by being with you, sharing life with you, and supporting you through your ups and downs. 

I have held onto this feeling for a long time, and you already know it. Today, I want to express it in a different way...  
I promise you that I will never let you down in any situation. I will always be happy with you and make sure you are happy all the time.  
You are my dream, my thought that I cannot erase, and my greatest happiness.  

If even a single look from you, or a small moment of attention on social media, can make me happy...  
imagine how joyful I would be if I had you for my whole life.  
I’m dreaming of a future with you.

“The universe whispers in cycles, showing us the same faces, the same souls, until we finally understand some connections are written in the stars, meant to return, meant to stay.”"""))
        st.session_state.messages.append(("bot", "✨ Will you be my love and shall we get married? ✨"))
        send_telegram(st.session_state.messages)
        st.session_state.step = "proposal"
        st.rerun()

    if col2.button("Hmm, okay..."):
        st.session_state.messages.append(("user", "Hmm, okay..."))
        st.session_state.messages.append(("bot", """💌 Ever since I met you, my world has felt brighter. 
Your smile, your presence, and everything about you makes my heart feel at home. 
I want that feeling forever by being with you, sharing life with you, and supporting you through your ups and downs. 

I have held onto this feeling for a long time, and you already know it. Today, I want to express it in a different way...  
I promise you that I will never let you down in any situation. I will always be happy with you and make sure you are happy all the time.  
You are my dream, my thought that I cannot erase, and my greatest happiness.  

If even a single look from you, or a small moment of attention on social media, can make me happy...  
imagine how joyful I would be if I had you for my whole life.  
I’m dreaming of a future with you.

“The universe whispers in cycles, showing us the same faces, the same souls, until we finally understand some connections are written in the stars, meant to return, meant to stay.”"""))
        st.session_state.messages.append(("bot", "✨ Will you be my love and shall we get married? ✨"))
        send_telegram(st.session_state.messages)
        st.session_state.step = "proposal"
        st.rerun()

elif st.session_state.step == "proposal":
    col1, col2, col3 = st.columns(3)
    if col1.button("❤️ Yes!"):
        st.session_state.messages.append(("user", "Yes! 💙"))
        st.session_state.messages.append(("bot", "🎉 Oh my goodness! GAYU is the happiest person alive right now! 😍"))
        send_telegram(st.session_state.messages)
        st.session_state.step = "yes"
        st.rerun()
    if col2.button("I need to think..."):
        st.session_state.messages.append(("user", "I need to think..."))
        st.session_state.messages.append(("bot", "That's completely okay. 😊 GAYU understands, feelings need time. 💙"))
        send_telegram(st.session_state.messages)
        st.session_state.step = "maybe"
        st.rerun()
    if col3.button("No"):
        st.session_state.messages.append(("user", "No"))
        st.session_state.messages.append(("bot", NO_RESPONSES[0]))
        st.session_state.no_count = 1
        send_telegram(st.session_state.messages)
        st.session_state.step = "no"
        st.rerun()

elif st.session_state.step == "maybe":
    col1, col2, col3 = st.columns(3)
    if col1.button("❤️ Actually, Yes!"):
        st.session_state.messages.append(("user", "Actually, Yes! 💙"))
        st.session_state.messages.append(("bot", "🎉 GAYU is over the moon! 😍 Thank you for giving love a chance!"))
        send_telegram(st.session_state.messages)
        st.session_state.step = "yes"
        st.rerun()
    if col2.button("Maybe later"):
        finish("That means the world to her. 🌟 GAYU will be right here, whenever you're ready.")
    if col3.button("No"):
        st.session_state.messages.append(("user", "No"))
        st.session_state.messages.append(("bot", NO_RESPONSES[0]))
        st.session_state.no_count = 1
        send_telegram(st.session_state.messages)
        st.session_state.step = "no"
        st.rerun()

elif st.session_state.step == "no":
    col1, col2 = st.columns(2)
    if col1.button("❤️ Okay, Yes!"):
        st.session_state.messages.append(("user", "Okay, Yes! 💙"))
        st.session_state.messages.append(("bot", "🎉 GAYU is OVER THE MOON right now! 😍"))
        send_telegram(st.session_state.messages)
        st.session_state.step = "yes"
        st.rerun()
    if col2.button("Still no"):
        nc = st.session_state.no_count
        if nc < len(NO_RESPONSES):
            st.session_state.messages.append(("user", "No"))
            st.session_state.messages.append(("bot", NO_RESPONSES[nc]))
            st.session_state.no_count += 1
            send_telegram(st.session_state.messages)
            st.rerun()
        else:
            finish("GAYU respects your decision. She wishes you all the happiness 💙")
