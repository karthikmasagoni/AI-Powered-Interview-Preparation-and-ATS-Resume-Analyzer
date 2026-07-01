import streamlit as st
import pandas as pd

from database import *
from quiz import QUESTIONS
from interview import get_questions
from resume_analyzer import analyze_resume
from resume_analyzer import extract_text_from_pdf
from groq_api import (
    get_ai_feedback,
    generate_interview_questions,
    evaluate_answer
)



init_db()



if "user" not in st.session_state:
    st.session_state.user = None



st.set_page_config(
    page_title="CareerBoost AI",
    page_icon="🎯",
    layout="wide"
)

st.title(
    "🎯 CareerPilot AI - Intelligent Placement Preparation Platform"
)



if st.session_state.user is None:

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if menu == "Register":

        if st.button(
            "Register"
        ):

            if register_user(
                username,
                password
            ):

                st.success(
                    "Registration Successful"
                )

            else:

                st.error(
                    "Username already exists"
                )

    else:

        if st.button(
            "Login"
        ):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.user = username

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )



else:

    st.sidebar.success(
        f"Welcome {st.session_state.user}"
    )

    if st.sidebar.button(
        "Logout"
    ):

        st.session_state.user = None

        st.rerun()

    page = st.sidebar.radio(
        "Features",
        [
            "Quiz",
            "Resume Analyzer",
            "Interview Prep",
            "Dashboard"
        ]
    )

    

    if page == "Quiz":

        st.header(
            "Aptitude Quiz"
        )

        score = 0

        answers = []

        for i, q in enumerate(
            QUESTIONS
        ):

            answer = st.radio(
                q["question"],
                q["options"],
                key=i
            )

            answers.append(
                answer
            )

        if st.button(
            "Submit Quiz"
        ):

            for q, a in zip(
                QUESTIONS,
                answers
            ):

                if a == q["answer"]:

                    score += 1

            percentage = (
                score
                /
                len(QUESTIONS)
            ) * 100

            save_score(
                st.session_state.user,
                score,
                percentage
            )

            st.success(
                f"Score: {score}/{len(QUESTIONS)}"
            )

            st.info(
                f"Percentage: {percentage:.2f}%"
            )

            st.progress(
                int(percentage)
            )

    

    elif page == "Resume Analyzer":

        st.header(
            "Resume Analyzer"
        )

        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"]
        )

        job_description = st.text_area(
            "Paste Job Description"
        )

        if uploaded_file and job_description:
            resume_text=extract_text_from_pdf(uploaded_file)

            result = analyze_resume(
                uploaded_file,
                job_description
            )

            st.metric(
                "ATS Match %",
                result[
                    "Match Percentage"
                ]
            )

            st.subheader(
                "Matched Keywords"
            )

            st.write(
                result[
                    "Matched Keywords"
                ]
            )

            st.subheader(
                "Missing Keywords"
            )

            st.write(
                result[
                    "Missing Keywords"
                ]
            )

            if st.button(
                "Generate AI Feedback"
            ):

                uploaded_file.seek(0)

                text = uploaded_file.read().decode(
                    errors="ignore"
                )

                feedback = get_ai_feedback(
                    resume_text,
                    job_description
                )

                st.write(
                    feedback
                )

    

    elif page == "Interview Prep":
    

        st.header("Interview Preparation")

        role = st.selectbox(
            "Select Role",
            ["AI/ML Engineer", "Python Developer", "Data Scientist"]
        )

        if "question" not in st.session_state:
            st.session_state.question = ""

        if st.button("Generate Question"):
            st.session_state.question = generate_interview_questions(role)

        if st.session_state.question:
            st.write(st.session_state.question)

            answer = st.text_area("Your Answer")

            if st.button("Evaluate Answer"):
                feedback = evaluate_answer(
                    st.session_state.question,
                    answer
                )
                st.success(feedback)

            if st.button("Next Question"):
                st.session_state.question = generate_interview_questions(role)
                st.rerun()



    elif page == "Dashboard":

        st.header(
            "Performance Dashboard"
        )

        data = get_scores(
            st.session_state.user
        )

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Score",
                    "Percentage"
                ]
            )

            st.dataframe(
                df
            )

            st.line_chart(
                df["Percentage"]
            )

            st.metric(
                "Best Percentage",
                f"{df['Percentage'].max():.2f}%"
            )

        else:

            st.info(
                "No quiz attempts found."
            )
