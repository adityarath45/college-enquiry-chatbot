"""
app.py - Streamlit web interface for the College Enquiry Chatbot
Author: Aditya Rath
Run with:  streamlit run app.py
"""

import streamlit as st
from chatbot import EnquiryBot

st.set_page_config(page_title="College Enquiry Chatbot", page_icon="🎓")

st.title("🎓 College Enquiry Assistant")
st.caption("Answers are based on reviewed FAQs. Project by Aditya Rath.")


# Load the chatbot only once (cache_resource keeps it in memory)
@st.cache_resource
def get_bot():
    return EnquiryBot("faqs.csv")


try:
    bot = get_bot()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not start the chatbot: {error}")
    st.stop()

# ---------- Session state: stores the chat history ----------
if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, message)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Try asking")
    sample_questions = [
        "How can I apply for admission?",
        "What is the fee structure?",
        "Does the college offer scholarships?",
        "Is hostel accommodation available?",
        "Does the college provide placement support?",
    ]
    clicked = None
    for q in sample_questions:
        if st.button(q, use_container_width=True):
            clicked = q

    st.divider()
    st.write(f"📚 FAQs loaded: **{len(bot.faqs)}**")
    st.write("Topics: " + ", ".join(sorted(bot.faqs["category"].unique())))
    if st.button("🗑️ Clear chat"):
        st.session_state.history = []
        st.rerun()

# ---------- Show previous messages ----------
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.write(message)

# ---------- Get new question (typed or clicked) ----------
typed = st.chat_input("Ask about admission, fees, hostel, placements...")
question = typed or clicked

if question and question.strip():
    answer, category, score = bot.get_answer(question)
    if category:
        answer = f"**[{category}]** {answer}"
    st.session_state.history.append(("user", question))
    st.session_state.history.append(("assistant", answer))
    st.rerun()

st.divider()
st.caption(
    "ℹ️ This chatbot is a student project prototype. Information is general - "
    "please confirm fees, dates and other details with the official college notices."
)
