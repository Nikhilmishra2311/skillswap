from sqlmodel import Session, select
from app.db.session import engine
from app.models.topic import Topic
from app.models.question import Question

with Session(engine) as db:
    topic = db.exec(
        select(Topic).where(Topic.name == "Trees")
    ).first()

    questions = [
        {"level":"beginner","question":"Binary tree max children?","option_a":"1","option_b":"2","option_c":"3","option_d":"4","correct_answer":"b"},
        {"level":"beginner","question":"Root node is?","option_a":"Top","option_b":"Leaf","option_c":"Middle","option_d":"None","correct_answer":"a"},

        {"level":"intermediate","question":"BST property?","option_a":"Left < Root < Right","option_b":"Random","option_c":"Equal","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"Traversal type?","option_a":"Inorder","option_b":"Preorder","option_c":"Postorder","option_d":"All","correct_answer":"d"},
        {"level":"intermediate","question":"Height of tree?","option_a":"Levels","option_b":"Nodes","option_c":"Edges","option_d":"None","correct_answer":"a"},

        {"level":"advanced","question":"AVL tree is?","option_a":"Balanced","option_b":"Unbalanced","option_c":"Graph","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Red-black tree ensures?","option_a":"Balance","option_b":"Sort","option_c":"Search","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Segment tree used for?","option_a":"Range query","option_b":"Sort","option_c":"Search","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Heap is?","option_a":"Tree","option_b":"Graph","option_c":"List","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Tree complexity?","option_a":"log n","option_b":"n","option_c":"n^2","option_d":"1","correct_answer":"a"},
    ]

    db.add_all([Question(topic_id=topic.id, **q) for q in questions])
    db.commit()

print("Tree questions added ✅")