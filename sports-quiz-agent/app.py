"""
AI-Powered Sports Quiz Generation Agent — Streamlit Dashboard

Run with: streamlit run app.py
"""

import streamlit as st
from quiz_generator import generate_quiz

st.set_page_config(page_title="Sports Quiz Agent", page_icon="🏆", layout="centered")

st.title("🏆 AI-Powered Sports Quiz Generation Agent")
st.caption(
    "Generates fresh, factually-grounded multiple-choice sports quizzes "
    "using RAG (ChromaDB) + live web search + an LLM."
)

SPORTS = ["Cricket", "Football", "Tennis", "Badminton", "Basketball"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

col1, col2 = st.columns(2)
with col1:
    sport = st.selectbox("Select a sport", SPORTS)
with col2:
    difficulty = st.selectbox("Select difficulty", DIFFICULTIES)

num_questions = st.slider("Number of questions", min_value=4, max_value=5, value=5)

if "quiz" not in st.session_state:
    st.session_state.quiz = None

button_col1, button_col2 = st.columns(2)
generate_clicked = button_col1.button("🎯 Generate Quiz", use_container_width=True)
regenerate_clicked = button_col2.button("🔄 Regenerate", use_container_width=True)

if generate_clicked or regenerate_clicked:
    with st.spinner("Retrieving grounding context and generating quiz..."):
        try:
            st.session_state.quiz = generate_quiz(sport, difficulty, num_questions)
        except Exception as e:
            st.error(f"Failed to generate quiz: {e}")
            st.session_state.quiz = None

quiz = st.session_state.quiz

if quiz:
    st.subheader(f"Sport: {quiz.get('sport', sport)}")
    st.write(f"**Difficulty:** {quiz.get('difficulty', difficulty)}")
    st.divider()

    for i, q in enumerate(quiz.get("questions", []), start=1):
        st.markdown(f"**Q{i}. {q['question']}**")
        for opt_key, opt_val in q["options"].items():
            st.write(f"{opt_key}. {opt_val}")

        with st.expander("Show answer & explanation"):
            correct = q["correct_answer"]
            st.success(f"Correct answer: {correct}. {q['options'].get(correct, '')}")
            st.write(q["explanation"])

        st.divider()
else:
    st.info("Select a sport and difficulty, then click **Generate Quiz** to begin.")

st.caption(
    "⚙️ Powered by ChromaDB (vector retrieval) + DuckDuckGo web search "
    "+ Claude (Anthropic API) for grounded quiz generation."
)
