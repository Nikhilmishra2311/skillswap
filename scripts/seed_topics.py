from sqlmodel import Session, select
from app.db.session import engine
from app.models.skill import Skill
from app.models.topic import Topic

topic_map = {
    "DSA": ["Arrays", "Trees", "Graphs", "DP"],
    "DBMS": ["SQL", "Normalization", "Transactions", "Indexing"],
    "CN": ["OSI Model", "TCP/IP", "Routing", "Subnetting"],
    "OS": ["Process", "Memory", "Scheduling", "Deadlock"]
}
existing = db.exec(
    select(Topic).where(
        Topic.name == topic_name,
        Topic.skill_id == skill.id
    )
).first()

if not existing:
    db.add(Topic(name=topic_name, skill_id=skill.id))
with Session(engine) as db:
    skills = db.exec(select(Skill)).all()

    for skill in skills:
        if skill.name in topic_map:
            for topic_name in topic_map[skill.name]:
                topic = Topic(name=topic_name, skill_id=skill.id)
                db.add(topic)

    db.commit()

print("Topics added successfully ✅")