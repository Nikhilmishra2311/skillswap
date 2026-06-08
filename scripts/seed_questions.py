from sqlmodel import Session, select
from app.db.session import engine
from app.models.question import Question
from app.models.topic import Topic


# 🔧 Helper function to insert questions
def add_questions(db, topic_id, questions):
    db.add_all([Question(topic_id=topic_id, **q) for q in questions])
    db.commit()


# 🧠 Topic-wise real questions
TOPIC_QUESTIONS = {

    # ================= DSA =================
    "Trees": [
        # Beginner
        {"level":"beginner","question":"In a Binary Tree, maximum children per node?","option_a":"1","option_b":"2","option_c":"3","option_d":"4","correct_answer":"b"},
        {"level":"beginner","question":"Root node is?","option_a":"Top node","option_b":"Leaf node","option_c":"Middle node","option_d":"None","correct_answer":"a"},

        # Intermediate
        {"level":"intermediate","question":"BST property is?","option_a":"Left < Root < Right","option_b":"Random","option_c":"Equal","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"Tree traversal includes?","option_a":"Inorder","option_b":"Preorder","option_c":"Postorder","option_d":"All","correct_answer":"d"},
        {"level":"intermediate","question":"Height of tree measures?","option_a":"Levels","option_b":"Nodes","option_c":"Edges","option_d":"None","correct_answer":"a"},

        # Advanced
        {"level":"advanced","question":"AVL tree ensures?","option_a":"Balanced tree","option_b":"Unbalanced","option_c":"Graph","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Red-black tree property?","option_a":"Balanced","option_b":"Unbalanced","option_c":"Graph","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Segment tree is used for?","option_a":"Range queries","option_b":"Sorting","option_c":"Searching","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Heap is?","option_a":"Tree-based structure","option_b":"Graph","option_c":"List","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Time complexity of balanced tree operations?","option_a":"O(log n)","option_b":"O(n)","option_c":"O(n^2)","option_d":"O(1)","correct_answer":"a"},
    ],

    "Arrays": [
        {"level":"beginner","question":"Array index starts from?","option_a":"0","option_b":"1","option_c":"-1","option_d":"None","correct_answer":"a"},
        {"level":"beginner","question":"Array is?","option_a":"Static data structure","option_b":"Dynamic","option_c":"Graph","option_d":"None","correct_answer":"a"},

        {"level":"intermediate","question":"Worst case search in array?","option_a":"O(n)","option_b":"O(log n)","option_c":"O(1)","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"Sorted array allows?","option_a":"Binary search","option_b":"DFS","option_c":"BFS","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"Insertion in array cost?","option_a":"O(n)","option_b":"O(1)","option_c":"O(log n)","option_d":"None","correct_answer":"a"},

        {"level":"advanced","question":"Kadane’s algorithm is used for?","option_a":"Max subarray sum","option_b":"Sorting","option_c":"Searching","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Prefix sum helps in?","option_a":"Range queries","option_b":"Sorting","option_c":"Graph","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Sliding window technique used for?","option_a":"Subarray problems","option_b":"Graph","option_c":"Tree","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Two pointer technique helps in?","option_a":"Optimized search","option_b":"Sorting","option_c":"Graph","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Merging arrays complexity?","option_a":"O(n)","option_b":"O(log n)","option_c":"O(n^2)","option_d":"O(1)","correct_answer":"a"},
    ],

    # ================= DBMS =================
    "SQL": [
        {"level":"beginner","question":"SQL stands for?","option_a":"Structured Query Language","option_b":"Simple Query","option_c":"Standard Query","option_d":"None","correct_answer":"a"},
        {"level":"beginner","question":"Primary key is?","option_a":"Unique","option_b":"Duplicate","option_c":"Null","option_d":"None","correct_answer":"a"},

        {"level":"intermediate","question":"JOIN is used for?","option_a":"Combine tables","option_b":"Delete data","option_c":"Insert","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"Index improves?","option_a":"Search performance","option_b":"Delete","option_c":"Insert","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"Normalization removes?","option_a":"Redundancy","option_b":"Tables","option_c":"Rows","option_d":"None","correct_answer":"a"},

        {"level":"advanced","question":"ACID properties ensure?","option_a":"Transaction reliability","option_b":"Speed","option_c":"Memory","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Deadlock occurs when?","option_a":"Circular wait","option_b":"No wait","option_c":"Single process","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"2PL ensures?","option_a":"Serializability","option_b":"Deadlock","option_c":"Loss","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"View is?","option_a":"Virtual table","option_b":"Physical table","option_c":"Index","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Trigger is?","option_a":"Auto action","option_b":"Manual","option_c":"Static","option_d":"None","correct_answer":"a"},
    ],

    # ================= CN =================
    "TCP/IP": [
        {"level":"beginner","question":"OSI layers count?","option_a":"5","option_b":"7","option_c":"6","option_d":"4","correct_answer":"b"},
        {"level":"beginner","question":"IP works at?","option_a":"Transport","option_b":"Network","option_c":"Data link","option_d":"Application","correct_answer":"b"},

        {"level":"intermediate","question":"TCP is?","option_a":"Connection-oriented","option_b":"Connectionless","option_c":"Both","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"UDP is used for?","option_a":"Speed","option_b":"Reliability","option_c":"Security","option_d":"None","correct_answer":"a"},
        {"level":"intermediate","question":"DNS converts?","option_a":"Name to IP","option_b":"IP to name","option_c":"Data","option_d":"None","correct_answer":"a"},

        {"level":"advanced","question":"TCP handshake steps?","option_a":"3","option_b":"2","option_c":"4","option_d":"5","correct_answer":"a"},
        {"level":"advanced","question":"HTTP is?","option_a":"Stateless","option_b":"Stateful","option_c":"Secure","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"MAC address is?","option_a":"Physical","option_b":"Logical","option_c":"Temporary","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Subnetting used for?","option_a":"Network division","option_b":"Security","option_c":"Routing","option_d":"None","correct_answer":"a"},
        {"level":"advanced","question":"Congestion control used in?","option_a":"TCP","option_b":"UDP","option_c":"IP","option_d":"None","correct_answer":"a"},
    ],
}


# 🚀 MAIN EXECUTION
with Session(engine) as db:

    topics = db.exec(select(Topic)).all()

    for topic in topics:
        print(f"Adding questions for topic: {topic.name}")

        # 👉 Use real questions if available
        questions = TOPIC_QUESTIONS.get(topic.name)

        # 👉 Fallback generic questions
        if not questions:
            questions = [
                {"level":"beginner","question":f"{topic.name}: Basic concept?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct_answer":"a"},
                {"level":"intermediate","question":f"{topic.name}: Working?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct_answer":"b"},
                {"level":"advanced","question":f"{topic.name}: Advanced concept?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct_answer":"c"},
            ]

        add_questions(db, topic.id, questions)

print("All topic-based questions added successfully ✅")