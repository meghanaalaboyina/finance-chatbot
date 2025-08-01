import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer (first time takes ~1GB)
@st.cache_resource
def load_model():
    model_name = "EleutherAI/gpt-neo-1.3B"  # Small, offline-compatible
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

st.title("💰 Personal Finance Chatbot")
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("Get personalized guidance on savings, taxes, and investments.")

user_type = st.selectbox("Who are you?", ["Student", "Professional"])
user_input = st.text_area("Ask me a financial question 👇")

if st.button("Get Advice") and user_input:
    with st.spinner("Thinking..."):
        prefix = f"You are a helpful financial advisor giving advice to a {user_type.lower()}.\n\nQuestion: {user_input}\nAnswer:"
        inputs = tokenizer(prefix, return_tensors="pt").to("cpu")

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

        reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = reply.split("Answer:")[-1].strip()

        # Show answer
        st.success(answer)

        # Save to chat history
        st.session_state.chat_history.append((user_input, answer))
        # Display chat history
        # Button to clear chat history
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")

if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("💬 Chat History")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"**A{i}:** {a}")

