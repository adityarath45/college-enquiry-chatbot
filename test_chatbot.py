"""Run: python test_chatbot.py  - checks the chatbot with different questions."""
from chatbot import EnquiryBot

bot = EnquiryBot()

# (question typed by user, expected category or None for fallback)
tests = [
    ("How can I apply for admission?", "Admissions"),
    ("how to apply for admission", "Admissions"),
    ("What documents do I need for admission?", "Admissions"),
    ("Do you have a hostel?", "Hostel"),
    ("hostel fees?", "Hostel"),
    ("What is the fee structure?", "Fees"),
    ("Is there any scholarship?", "Scholarships"),
    ("How can I get a scholarship?", "Scholarships"),
    ("Tell me about placements", "Placements"),
    ("what is the average package", "Placements"),
    ("Which courses are available?", "Courses"),
    ("How do I contact the college?", "Contact"),
    ("When is the exam?", "Examinations"),
    ("admision procces", None),            # heavy spelling mistakes
    ("Tell me a joke", None),
    ("What is the weather today?", None),
    ("Who won the cricket match?", None),
    ("what is your name", None),
    ("hostel", "Hostel"),
    ("is there a library in college", "Facilities"),
    ("last date for admission", "Admissions"),
    ("do you have bus facility", "Facilities"),
    ("how much money do I need to pay", "Fees"),   # meaning-based, hard for TF-IDF
    ("I want to join your college", "Admissions"), # meaning-based, hard for TF-IDF
    ("   ", None),
    ("?????", None),
]

passed = 0
for q, expected in tests:
    answer, category, score = bot.get_answer(q)
    ok = (category == expected)
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'} | {q!r:45} | got={category} | score={score:.2f} | expected={expected}")
print(f"\n{passed}/{len(tests)} tests passed")
