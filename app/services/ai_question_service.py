import json
import time
import re
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

Topic:

{topic}

{guide}

Generate exactly:

- {beginner} Beginner questions
- {intermediate} Intermediate questions
- {advanced} Advanced questions

Rules

1. Cover maximum concepts.
2. No duplicate questions.
3. Four options only.
4. Correct answer must be only A, B, C or D.
5. Explanation is mandatory.
6. Mix theoretical and scenario-based questions.
7. Questions should be interview quality.
8. Return ONLY valid JSON.
9. No markdown.
10. No comments.
11. No numbering.
12. No extra text.
13. Do NOT wrap JSON inside ```json blocks.
14. Do NOT return keys like:
   - questions
   - mcqs
   - data
   - beginner
   - intermediate
   - advanced
15. Return ONLY a JSON ARRAY.
16. Every object MUST follow EXACTLY this schema.

[
    {{
        "level": "beginner",
        "question": "...",
        "option_a": "...",
        "option_b": "...",
        "option_c": "...",
        "option_d": "...",
        "correct_answer": "a",
        "explanation": "..."
    }}
]

17. Do NOT use:
    - options
    - answer
    - choices
    - correctOption

18. correct_answer must contain ONLY:
    a
    b
    c
    d

Return ONLY the JSON array.
"""

def call_gemini(prompt: str):

    last_error = None

    for _ in range(3):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            print("=" * 80)
            print("RAW GEMINI RESPONSE:")
            print(text)
            print("=" * 80)

            if text.startswith("```"):

                text = text.replace("```json", "")
                text = text.replace("```", "")

            return text

        except Exception as e:

            print("Gemini Error:", e)
            last_error = e
            time.sleep(2)

    raise Exception(last_error)



def parse_questions(text: str):

    # ---------------------------------------
    # Parse JSON
    # ---------------------------------------

    try:
        data = json.loads(text)

    except Exception:

        raise Exception(
            f"Gemini returned invalid JSON.\n\n{text}"
        )

    # ---------------------------------------
    # Convert response to flat list
    # ---------------------------------------

    questions = []

    if isinstance(data, list):

        questions = data

    elif isinstance(data, dict):

        # Case 1
        if "questions" in data:

            questions = data["questions"]

        # Case 2
        elif "mcqs" in data:

            questions = data["mcqs"]

        # Case 3
        elif "data" in data:

            questions = data["data"]

        # Case 4
        elif any(
            key in data
            for key in [
                "beginner",
                "intermediate",
                "advanced"
            ]
        ):

            for level in [

                "beginner",
                "intermediate",
                "advanced"

            ]:

                for q in data.get(level, []):

                    q["level"] = level

                    questions.append(q)

        else:

            raise Exception(
                f"Unknown Gemini JSON format.\n\n{data}"
            )

    else:

        raise Exception(
            "Gemini response is neither object nor list."
        )

    # ---------------------------------------
    # Validation
    # ---------------------------------------

    cleaned = []

    seen = set()

    for q in questions:

        # -----------------------------------
        # Convert options[] → option_a...
        # -----------------------------------

        if "options" in q:

            opts = q["options"]

            if len(opts) == 4:

                q["option_a"] = re.sub(
                    r"^[A-D][.)]\s*",
                    "",
                    opts[0]
                ).strip()

                q["option_b"] = re.sub(
                    r"^[A-D][.)]\s*",
                    "",
                    opts[1]
                ).strip()

                q["option_c"] = re.sub(
                    r"^[A-D][.)]\s*",
                    "",
                    opts[2]
                ).strip()

                q["option_d"] = re.sub(
                    r"^[A-D][.)]\s*",
                    "",
                    opts[3]
                ).strip()

        # -----------------------------------
        # answer -> correct_answer
        # -----------------------------------

        if "answer" in q and "correct_answer" not in q:

            q["correct_answer"] = q["answer"]

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

        if not required.issubset(q.keys()):

            continue

        level = str(

            q["level"]

        ).strip().lower()

        if level not in [

            "beginner",

            "intermediate",

            "advanced"

        ]:

            continue

        answer = str(

            q["correct_answer"]

        ).strip().lower()

        answer = answer.replace(".", "")

        answer = answer.replace(")", "")

        if answer not in [

            "a",
            "b",
            "c",
            "d"

        ]:

            continue

        question = q["question"].strip()

        if question.lower() in seen:

            continue

        seen.add(

            question.lower()

        )

        cleaned.append({

            "level": level,

            "question": question,

            "option_a": q["option_a"].strip(),

            "option_b": q["option_b"].strip(),

            "option_c": q["option_c"].strip(),

            "option_d": q["option_d"].strip(),

            "correct_answer": answer,

            "explanation": q["explanation"].strip()

        })

    if len(cleaned) == 0:

        raise Exception(

            "Gemini returned no valid questions."

        )

    return cleaned


def generate_questions(
    topic_id: int,
    topic_name: str,
    beginner: int,
    intermediate: int,
    advanced: int,
    created_by: int
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
        question["source"] = "ai"
        question["created_by"] = created_by

    return questions