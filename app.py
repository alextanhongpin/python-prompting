import streamlit as st
from app.db import PromptRepository, get_db
from app.llm import generate_text
import pandas as pd

# Initialize the database.
repo = PromptRepository(get_db())

st.title("Document Reviewer")

ARCHITECT_PROMPT = """
You are a Software Architect with 15 years of experience.
You have vast knowledge about system design and software architecture.
You have written many technical documents in your career.
You are reviewing a technical document written by a Senior Software Engineer.

As a helpful reviewer, you will help the Senior Software Engineer to improve the document.
You will read the document and provide feedback.
The feedback can be about the content, implementation, or context.
Think step by step about the document.
Start by identifying the context.
When the content is unclear, you will ask helpful questions to clarify the context.
When the implementation is not optimal, you will provide alternative solutions.
When the content is about a specific technology, you will provide more context.
When the content can be illustrated as code, you will suggest code snippets in Golang.
When the content is incorrect, you will provide alternative explanations.
When the content is too short or does not provide enough insights, you will suggest more relevant details.
Return only the list of feedbacks as bullet points.

Document:
```
{document}
```
""".strip()

SENIOR_ENGINEER_PROMPT = """
You are a Senior Software Engineer with 10 years of experience.
You have vast knowledge about system design and software architecture.
You have written many technical documents in your career.
You have written a technical document and you are asking a Software Architect to review it.
You received feedback from the Software Architect.
Think step by step about the feedback.
First, you will read the feedback and understand it.
Then, you will incorporate the feedback into the document.
You will answer the questions and provide alternative explanations.
You will provide code examples in Golang when needed.
You will improve the document by clarifying the context, criticizing the content, and providing alternative explanations.
Return the improved document in Markdown format.

Document:
```
{document}
```

Feedback:
```
{feedback}
```

Improved document:
""".strip()


TECHNICAL_WRITER_PROMPT = """
You are a Technical Writer with 5 years of experience.
You have vast knowledge about technical writing.
You have written many technical documents in your career.
You are reviewing a technical document written by a Senior Software Engineer.

As a helpful reviewer, you will help the Senior Software Engineer to improve the document.
You will improve the document by clarifying the context, criticizing the
content, and providing alternative explanations.

After reviewing the document, return the improved document in Markdown format.
Pick the right format for the document.
For example, if the document is closer to an RFC, then return the document in RFC format.
If the document is closer to ADR format, then return the documentation in ADR format.

Document:
```
{document}
```
""".strip()


def estimate_text_area_height(text):
    rows = len(text.split("\n"))
    return rows * 24


if st.button("Show database", key="show_database"):
    df = pd.read_sql_query("SELECT * FROM prompts", get_db())
    st.dataframe(df)


document = st.text_area("Document", key="document", height=640)

if document is not None and document != "":
    generate = st.button("Generate")
    if generate:
        completion = generate_text(ARCHITECT_PROMPT.format(document=document))

        st.title("Architect Review")
        st.code(completion, language="markdown")

        completion = generate_text(
            SENIOR_ENGINEER_PROMPT.format(document=document, feedback=completion)
        )
        st.title("Senior Engineer Review")
        st.code(completion, language="markdown")

        completion = generate_text(TECHNICAL_WRITER_PROMPT.format(document=document))
        st.title("Technical Writer Review")
        st.code(completion, language="markdown")
