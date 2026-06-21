from sqlmodel import Session, select
from app.db.session import engine
from app.models.question import Question
from app.models.topic import Topic


# 🔧 Helper function to insert questions
def add_questions(db, topic_id, questions):

    existing = db.exec(
        select(Question).where(
            Question.topic_id == topic_id
        )
    ).first()

    if existing:
        print(f"Questions already exist for topic_id={topic_id}")
        return

    db.add_all(
        [Question(topic_id=topic_id, **q) for q in questions]
    )
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
    "Graphs": [
    {"level":"beginner","question":"Graph consists of?","option_a":"Vertices and Edges","option_b":"Nodes only","option_c":"Edges only","option_d":"Arrays","correct_answer":"a"},
    {"level":"beginner","question":"Graph can be?","option_a":"Directed","option_b":"Undirected","option_c":"Both","option_d":"None","correct_answer":"c"},

    {"level":"intermediate","question":"BFS uses?","option_a":"Queue","option_b":"Stack","option_c":"Array","option_d":"Heap","correct_answer":"a"},
    {"level":"intermediate","question":"DFS uses?","option_a":"Queue","option_b":"Stack","option_c":"Array","option_d":"Tree","correct_answer":"b"},
    {"level":"intermediate","question":"Shortest path algorithm?","option_a":"Dijkstra","option_b":"Merge Sort","option_c":"Binary Search","option_d":"Heap","correct_answer":"a"},

    {"level":"advanced","question":"Topological sorting works on?","option_a":"DAG","option_b":"Tree","option_c":"Array","option_d":"Heap","correct_answer":"a"},
    {"level":"advanced","question":"MST stands for?","option_a":"Minimum Spanning Tree","option_b":"Maximum Search Tree","option_c":"Minimum Search Tree","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Prim's algorithm finds?","option_a":"MST","option_b":"Shortest Path","option_c":"Cycle","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Kruskal's algorithm uses?","option_a":"Union Find","option_b":"Queue","option_c":"Stack","option_d":"Array","correct_answer":"a"},
    {"level":"advanced","question":"Bellman Ford handles?","option_a":"Negative Weights","option_b":"Sorting","option_c":"Searching","option_d":"None","correct_answer":"a"},
],

"HashMap": [
    {"level":"beginner","question":"HashMap stores data in?","option_a":"Key-Value Pair","option_b":"Array","option_c":"Tree","option_d":"Graph","correct_answer":"a"},
    {"level":"beginner","question":"Keys in HashMap are?","option_a":"Unique","option_b":"Duplicate","option_c":"Null only","option_d":"Sorted","correct_answer":"a"},

    {"level":"intermediate","question":"Average search complexity?","option_a":"O(1)","option_b":"O(n)","option_c":"O(log n)","option_d":"O(n²)","correct_answer":"a"},
    {"level":"intermediate","question":"Collision means?","option_a":"Same hash index","option_b":"Same value","option_c":"Same key","option_d":"None","correct_answer":"a"},
    {"level":"intermediate","question":"Java HashMap is part of?","option_a":"Collections Framework","option_b":"IO","option_c":"JDBC","option_d":"AWT","correct_answer":"a"},

    {"level":"advanced","question":"Collision resolution technique?","option_a":"Chaining","option_b":"Sorting","option_c":"Recursion","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Load factor default value?","option_a":"0.75","option_b":"0.5","option_c":"1","option_d":"2","correct_answer":"a"},
    {"level":"advanced","question":"Rehashing occurs when?","option_a":"Threshold exceeds","option_b":"Delete","option_c":"Search","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"HashMap allows null key?","option_a":"Yes","option_b":"No","option_c":"Sometimes","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Worst case complexity?","option_a":"O(n)","option_b":"O(1)","option_c":"O(log n)","option_d":"O(n²)","correct_answer":"a"},
],

"Linked List": [
    {"level":"beginner","question":"Linked List stores data using?","option_a":"Nodes","option_b":"Arrays","option_c":"Graphs","option_d":"Trees","correct_answer":"a"},
    {"level":"beginner","question":"Each node contains?","option_a":"Data and Pointer","option_b":"Only Data","option_c":"Only Pointer","option_d":"Index","correct_answer":"a"},

    {"level":"intermediate","question":"Insertion at head complexity?","option_a":"O(1)","option_b":"O(n)","option_c":"O(log n)","option_d":"O(n²)","correct_answer":"a"},
    {"level":"intermediate","question":"Traversal complexity?","option_a":"O(n)","option_b":"O(1)","option_c":"O(log n)","option_d":"O(n²)","correct_answer":"a"},
    {"level":"intermediate","question":"Doubly Linked List has?","option_a":"Two pointers","option_b":"One pointer","option_c":"No pointer","option_d":"Three pointers","correct_answer":"a"},

    {"level":"advanced","question":"Cycle detection algorithm?","option_a":"Floyd's","option_b":"Dijkstra","option_c":"Prim's","option_d":"Kruskal","correct_answer":"a"},
    {"level":"advanced","question":"Fast and Slow pointer used for?","option_a":"Cycle Detection","option_b":"Sorting","option_c":"Searching","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Merge two sorted linked lists complexity?","option_a":"O(n)","option_b":"O(log n)","option_c":"O(1)","option_d":"O(n²)","correct_answer":"a"},
    {"level":"advanced","question":"Reverse linked list complexity?","option_a":"O(n)","option_b":"O(1)","option_c":"O(log n)","option_d":"O(n²)","correct_answer":"a"},
    {"level":"advanced","question":"Middle node finding complexity?","option_a":"O(n)","option_b":"O(1)","option_c":"O(log n)","option_d":"O(n²)","correct_answer":"a"},
],

"OSI Model": [
    {"level":"beginner","question":"OSI model has how many layers?","option_a":"5","option_b":"6","option_c":"7","option_d":"8","correct_answer":"c"},
    {"level":"beginner","question":"Top layer of OSI?","option_a":"Application","option_b":"Transport","option_c":"Network","option_d":"Session","correct_answer":"a"},

    {"level":"intermediate","question":"Transport layer protocol?","option_a":"TCP","option_b":"IP","option_c":"ARP","option_d":"ICMP","correct_answer":"a"},
    {"level":"intermediate","question":"Network layer handles?","option_a":"Routing","option_b":"Encryption","option_c":"Compression","option_d":"Storage","correct_answer":"a"},
    {"level":"intermediate","question":"Data Link layer uses?","option_a":"MAC Address","option_b":"IP Address","option_c":"Port","option_d":"URL","correct_answer":"a"},

    {"level":"advanced","question":"Presentation layer handles?","option_a":"Encryption","option_b":"Routing","option_c":"Switching","option_d":"Caching","correct_answer":"a"},
    {"level":"advanced","question":"Session layer responsible for?","option_a":"Connection Management","option_b":"Routing","option_c":"Storage","option_d":"Addressing","correct_answer":"a"},
    {"level":"advanced","question":"PDU of Transport Layer?","option_a":"Segment","option_b":"Packet","option_c":"Frame","option_d":"Bit","correct_answer":"a"},
    {"level":"advanced","question":"PDU of Network Layer?","option_a":"Packet","option_b":"Segment","option_c":"Frame","option_d":"Bit","correct_answer":"a"},
    {"level":"advanced","question":"PDU of Data Link Layer?","option_a":"Frame","option_b":"Packet","option_c":"Segment","option_d":"Bit","correct_answer":"a"},
],

"Normalization": [
    {"level":"beginner","question":"Normalization removes?","option_a":"Redundancy","option_b":"Rows","option_c":"Columns","option_d":"Tables","correct_answer":"a"},
    {"level":"beginner","question":"1NF removes?","option_a":"Repeating Groups","option_b":"Dependency","option_c":"Keys","option_d":"Indexes","correct_answer":"a"},

    {"level":"intermediate","question":"2NF removes?","option_a":"Partial Dependency","option_b":"Transitive Dependency","option_c":"Redundancy","option_d":"Joins","correct_answer":"a"},
    {"level":"intermediate","question":"3NF removes?","option_a":"Transitive Dependency","option_b":"Partial Dependency","option_c":"Keys","option_d":"Indexes","correct_answer":"a"},
    {"level":"intermediate","question":"BCNF is stricter than?","option_a":"3NF","option_b":"2NF","option_c":"1NF","option_d":"None","correct_answer":"a"},

    {"level":"advanced","question":"Normalization improves?","option_a":"Data Integrity","option_b":"Redundancy","option_c":"Duplication","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Denormalization is used for?","option_a":"Performance","option_b":"Integrity","option_c":"Security","option_d":"Backup","correct_answer":"a"},
    {"level":"advanced","question":"Functional dependency defines?","option_a":"Attribute relationship","option_b":"Joins","option_c":"Views","option_d":"Indexes","correct_answer":"a"},
    {"level":"advanced","question":"Candidate key is?","option_a":"Minimal Super Key","option_b":"Primary Key","option_c":"Foreign Key","option_d":"None","correct_answer":"a"},
    {"level":"advanced","question":"Super key can have?","option_a":"Extra attributes","option_b":"No attributes","option_c":"Only one attribute","option_d":"None","correct_answer":"a"},
],
"string": [

    # Beginner
    {
        "level":"beginner",
        "question":"String is?",
        "option_a":"Sequence of characters",
        "option_b":"Number",
        "option_c":"Array only",
        "option_d":"Function",
        "correct_answer":"a" },
    {
        "level":"beginner",
        "question":"Which class represents strings in Java?",
        "option_a":"String",
        "option_b":"Char",
        "option_c":"Text",
        "option_d":"Object",
        "correct_answer":"a"
    },

    # Intermediate
    {
        "level":"intermediate",
        "question":"String objects are?",
        "option_a":"Mutable",
        "option_b":"Immutable",
        "option_c":"Dynamic",
        "option_d":"None",
        "correct_answer":"b"
    },
    {
        "level":"intermediate",
        "question":"Which method returns string length?",
        "option_a":"size()",
        "option_b":"count()",
        "option_c":"length()",
        "option_d":"getLength()",
        "correct_answer":"c"
    },
    {
        "level":"intermediate",
        "question":"StringBuilder is used because?",
        "option_a":"Mutable strings",
        "option_b":"Immutable strings",
        "option_c":"Arrays",
        "option_d":"Sorting",
        "correct_answer":"a"
    },

    # Advanced
    {
        "level":"advanced",
        "question":"Time complexity of string concatenation using '+' repeatedly?",
        "option_a":"O(n²)",
        "option_b":"O(log n)",
        "option_c":"O(1)",
        "option_d":"O(n)",
        "correct_answer":"a"
    },
    {
        "level":"advanced",
        "question":"Which algorithm is used for pattern matching?",
        "option_a":"KMP",
        "option_b":"DFS",
        "option_c":"BFS",
        "option_d":"Dijkstra",
        "correct_answer":"a"
    },
    {
        "level":"advanced",
        "question":"Longest Palindromic Substring belongs to?",
        "option_a":"String Problems",
        "option_b":"Graph",
        "option_c":"Tree",
        "option_d":"Heap",
        "correct_answer":"a"
    },
    {
        "level":"advanced",
        "question":"String interning is related to?",
        "option_a":"String Pool",
        "option_b":"Heap Sort",
        "option_c":"HashMap",
        "option_d":"Queue",
        "correct_answer":"a"
    },
    {
        "level":"advanced",
        "question":"Rabin-Karp algorithm uses?",
        "option_a":"Hashing",
        "option_b":"Recursion",
        "option_c":"Greedy",
        "option_d":"DP",
        "correct_answer":"a"
    }
]
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