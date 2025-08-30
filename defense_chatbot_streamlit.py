import os
import json
from datetime import datetime
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


load_dotenv()  # load .env file

client = Groq(api_key=os.getenv("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"))

# Use API key from .env
#client = Groq(api_key=os.getenv("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"))

LOG_FILE = "defense_chatbot_feedback.json"

# --- Helper Functions ---
def answer_defense_question(user_input):
    """Answer factual defense/military questions"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # or "llama-3.1-8b-instant" for faster
        messages=[
            {"role": "system", "content": "You are a military defense expert who provides clear and accurate answers."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=400
    )
    return response.choices[0].message.content.strip()


def generate_defense_questions(topic):
    """Generate multiple-choice practice questions"""
    prompt = f"Generate 3 multiple-choice questions (with 4 options each) about {topic} in the field of military and defense. Provide the correct answer after each question."
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # using Groq model, faster for generation
        messages=[
            {"role": "system", "content": "You are a military instructor who creates defense-related quiz questions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


def log_feedback(entry):
    """Store question, answer, and feedback in a JSON file"""
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --- Streamlit App ---
st.set_page_config(page_title="🪖 Military & Defense Chatbot", layout="wide")
st.title("🪖 Military & Defense AI Chatbot")

menu = st.sidebar.radio("Choose Function", ["Ask a Question", "Generate Practice Questions"])

if menu == "Ask a Question":
    st.subheader("📘 Ask a Defense-related Question")
    user_q = st.text_input("Enter your question:")
    if st.button("Get Answer") and user_q.strip():
        answer = answer_defense_question(user_q)
        st.markdown("### 📘 Answer:")
        st.write(answer)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Helpful"):
                log_feedback({
                    "type": "Answer",
                    "question": user_q,
                    "response": answer,
                    "feedback": "yes",
                    "timestamp": datetime.utcnow().isoformat()
                })
                st.success("Feedback recorded: Helpful ✅")
        with col2:
            if st.button("👎 Not Helpful"):
                log_feedback({
                    "type": "Answer",
                    "question": user_q,
                    "response": answer,
                    "feedback": "no",
                    "timestamp": datetime.utcnow().isoformat()
                })
                st.error("Feedback recorded: Not Helpful ❌")

elif menu == "Generate Practice Questions":
    st.subheader("📝 Generate Military/Defense Practice Questions")
    topic = st.text_input("Enter a defense topic (e.g., Indian Army, NATO, Cybersecurity):")
    if st.button("Generate") and topic.strip():
        questions = generate_defense_questions(topic)
        st.markdown("### 📝 Practice Questions:")
        st.write(questions)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Good Questions"):
                log_feedback({
                    "type": "PracticeQuestions",
                    "topic": topic,
                    "response": questions,
                    "feedback": "yes",
                    "timestamp": datetime.utcnow().isoformat()
                })
                st.success("Feedback recorded: Good ✅")
        with col2:
            if st.button("👎 Poor Questions"):
                log_feedback({
                    "type": "PracticeQuestions",
                    "topic": topic,
                    "response": questions,
                    "feedback": "no",
                    "timestamp": datetime.utcnow().isoformat()
                })
                st.error("Feedback recorded: Poor ❌")
