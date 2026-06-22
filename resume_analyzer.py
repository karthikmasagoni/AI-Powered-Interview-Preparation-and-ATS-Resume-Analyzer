
from pypdf import PdfReader
import re


def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text.lower()


def analyze_resume(
    uploaded_file,
    job_description
):

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

    keywords = list(
        set(
            re.findall(
                r"[A-Za-z+#.]+",
                job_description.lower()
            )
        )
    )

    matched_keywords = []

    for keyword in keywords:

        if keyword in resume_text:

            matched_keywords.append(
                keyword
            )

    missing_keywords = list(
        set(keywords)
        -
        set(matched_keywords)
    )

    if len(keywords) > 0:

        match_percentage = (
            len(matched_keywords)
            /
            len(keywords)
        ) * 100

    else:

        match_percentage = 0

    suggestions = []

    for skill in missing_keywords[:10]:

        suggestions.append(
            f"Consider adding experience with {skill}"
        )

    return {

        "Match Percentage":
            round(
                match_percentage,
                2
            ),

        "Matched Keywords":
            matched_keywords,

        "Missing Keywords":
            missing_keywords,

        "Suggestions":
            suggestions
    }