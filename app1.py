import streamlit as st
import google.generativeai as genai
import random

# ------------- GOOGLE GENAI SETUP -------------
genai.configure(api_key="AIzaSyBd5xlrY1-rdzMGrefILn8HXx40k3fTZTk")  # 🔐 Replace this with your Gemini API key
model = genai.GenerativeModel("gemini-2.5-pro")

# ------------- PAGE CONFIGURATION -------------
st.set_page_config(
    page_title="💸 AI Finance Advisor",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------- CUSTOM CSS STYLING -------------
st.markdown("""
    <style>
    html, body {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        background: linear-gradient(to right, #00b4db, #0083b0);
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #444;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .chat-bubble {
        background-color: #ffffff;
        padding: 1rem;
        border-left: 5px solid #00b4db;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .chat-bubble h5 {
        margin: 0;
    }
    .user-msg {
        font-weight: bold;
        color: #333;
    }
    .bot-msg {
        margin-top: 0.5rem;
        color: #000;
    }
    .stButton>button {
        background-color: #0083b0;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        height: 3em;
        width: 10em;
        margin: 0.5em;
    }
    .stButton>button:hover {
        background-color: #005f73;
    }
    </style>
""", unsafe_allow_html=True)

# ------------- DYNAMIC QUOTE HEADER -------------
quotes = [
    "“Do not save what is left after spending, but spend what is left after saving.” — Warren Buffett",
    "“A budget is telling your money where to go instead of wondering where it went.” — Dave Ramsey",
    "“It's not your salary that makes you rich, it's your spending habits.” — Charles A. Jaffe",
]
quote = random.choice(quotes)

st.markdown("<div class='main-title'>💰 Smart Finance Chatbot</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>💡 {quote}</div>", unsafe_allow_html=True)

# ------------- SESSION STATE INIT -------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------- USER INPUT SECTION -------------
st.subheader("🎯 Who are you?")
user_type = st.selectbox("", ["Student", "Professional", "Freelancer", "Parent", "Investor"])

user_input = st.text_area("💬 Ask your financial question:", placeholder="e.g., How can I build an emergency fund?")

col1, col2 = st.columns([1, 1])
with col1:
    send = st.button("📨 Get Advice")
with col2:
    clear = st.button("🧹 Clear Chat")

# ------------- HANDLE GENERATION -------------
if send and user_input.strip():
    with st.spinner("💡 Gemini is thinking..."):
        prompt = f"""You are a helpful personal finance advisor for a {user_type.lower()}.
Answer clearly and in a friendly, easy-to-understand way.

User: {user_input}
Advisor:"""
        try:
            response = model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            answer = f"⚠ Error: {str(e)}"

        st.session_state.chat_history.insert(0, (user_input, answer))
        st.success("✅ Answer generated!")

# ------------- HANDLE CLEARING -------------
if clear:
    st.session_state.chat_history = []
    st.success("🧼 Chat history cleared!")

# ------------- DISPLAY CHAT -------------
if st.session_state.chat_history:
    st.markdown("## 🗂 Chat History")
    for i, (q, a) in enumerate(st.session_state.chat_history, 1):
        st.markdown(f"""
            <div class='chat-bubble'>
                <h5>🧑‍💼 <span class='user-msg'>Q{i}: {q}</span></h5>
                <div class='bot-msg'>🤖 {a}</div>
            </div>
        """, unsafe_allow_html=True)