from sqlmodel import Session, select

from app.db.session import engine
from app.models.topic import Topic

TOPICS = [
    # DSA
    "Arrays",
    "Trees",
    "Graphs",
    "DP",
    "Linked List",
    "Stack",
    "Queue",
    "HashMap",

    # DBMS
    "SQL",
    "Normalization",
    "Transactions",
    "Indexing",
    "Joins",

    # CN
    "TCP/IP",
    "OSI Model",
    "Routing",
    "Subnetting",
    "DNS",

    # OS
    "Process",
    "Memory",
    "Scheduling",
    "Deadlock"
]

with Session(engine) as db:

    for topic_name in TOPICS:

        existing = db.exec(
            select(Topic).where(
                Topic.name == topic_name
            )
        ).first()

        if not existing:
            db.add(
                Topic(name=topic_name)
            )

    db.commit()

print("Topics added successfully ✅")