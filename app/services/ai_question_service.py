import json
import time

import google.generativeai as genai

from app.core.config import settings


genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

TOPIC_GUIDE = {

    "Java": """
Cover:
- OOP
- JVM
- JDK
- JRE
- Collections
- Multithreading
- Streams
- Exception Handling
- Memory Management
- Java 8 Features
""",

    "DBMS": """
Cover:
- Normalization
- Transactions
- ACID
- SQL
- Joins
- Indexing
- Locking
- Views
- Stored Procedures
""",

    "Computer Networks": """
Cover:
- OSI
- TCP/IP
- HTTP
- HTTPS
- DNS
- Routing
- Switching
- Congestion
- SSL
""",

    "Operating System": """
Cover:
- Process
- Thread
- Scheduling
- Deadlock
- Paging
- Virtual Memory
- Synchronization
""",

    "Python": """
Cover:
- OOP
- Decorators
- Generators
- GIL
- Exception Handling
- Iterators
- AsyncIO
"""
}
def build_prompt(

    topic,

    beginner,

    intermediate,

    advanced

):

    guide = TOPIC_GUIDE.get(

        topic,

        ""

    )

    return f"""
You are an experienced Technical Interviewer.

Generate interview-quality MCQs.

Topic

{topic}

{guide}

Generate

{beginner} Beginner

{intermediate} Intermediate

{advanced} Advanced

Rules

1. Cover maximum concepts.

2. No duplicate questions.

3. Four options only.

4. Correct answer should be A/B/C/D.

5. Explanation mandatory.

6. Return ONLY valid JSON.

7. No markdown.

8. No comments.

9. No numbering.

10. Mix theoretical and scenario-based questions.
"""


def call_gemini(prompt: str):

    last_error = None

    for _ in range(3):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            if text.startswith("```"):

                text = text.replace("```json", "")

                text = text.replace("```", "")

            return text

        except Exception as e:

            last_error = e

            time.sleep(2)

    raise Exception(last_error)




def parse_questions(text: str):

    try:

        questions = json.loads(text)

    except Exception:

        raise Exception("Gemini returned invalid JSON.")

    if not isinstance(questions, list):

        raise Exception("Gemini should return a list.")

    required = {

        "level",
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
        "explanation"

    }

    cleaned = []

    seen = set()

    for q in questions:

        if not required.issubset(q.keys()):
            continue

        level = q["level"].lower().strip()

        if level not in [

            "beginner",

            "intermediate",

            "advanced"

        ]:

            continue

        answer = q["correct_answer"].lower()

        if answer not in [

            "a",

            "b",

            "c",

            "d"

        ]:

            continue

        duplicate = (

            q["question"]

            .strip()

            .lower()

        )

        if duplicate in seen:

            continue

        seen.add(duplicate)

        cleaned.append({

            "level": level,

            "question": q["question"].strip(),

            "option_a": q["option_a"].strip(),

            "option_b": q["option_b"].strip(),

            "option_c": q["option_c"].strip(),

            "option_d": q["option_d"].strip(),

            "correct_answer": answer,

            "explanation": q["explanation"].strip()

        })

    return cleaned

def generate_questions(

    topic_id: int,

    topic_name: str,

    beginner: int,

    intermediate: int,

    advanced: int

):

    prompt = build_prompt(

        topic_name,

        beginner,

        intermediate,

        advanced

    )

    response = call_gemini(prompt)

    questions = parse_questions(response)

    for question in questions:

        question["topic_id"] = topic_id

    return questions