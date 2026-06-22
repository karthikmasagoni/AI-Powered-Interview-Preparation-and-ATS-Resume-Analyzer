from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client=Groq(api_key="GROQ_API_KEY")


def get_ai_feedback(
    resume_text,
    job_description
):

    prompt = f"""
    Analyze this resume.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:

    1. ATS Match Analysis
    2. Missing Skills
    3. Resume Improvements
    4. Resume Score out of 100
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_interview_questions(
    role
):

    prompt = f"""
    Generate only one interview questions
    for {role}. Do not generate multiple questions,
    Include technical and HR questions.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def evaluate_answer(question,answer):
    prompt=f"""
    Interview Question:{question}
    Candidate Answer:{answer}

    Evaluate:
    1.Score out of 10
    2.Strength
    3.Weaknesses
    4.Better Answer """

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content