# 🎓 AI-Powered College Enquiry System

A simple chatbot that answers common college questions (admissions, courses, fees,
scholarships, placements, hostel and more) using NLP.

**Author:** Aditya Rath
**Domain:** Artificial Intelligence / NLP | **Minor Project** (Internship)

## How it works
1. The user types a question in the Streamlit chat box.
2. The text is cleaned (lowercase, punctuation removed).
3. **TF-IDF** converts the question and all FAQ questions into numbers.
4. **Cosine Similarity** finds the most similar FAQ.
5. If the similarity is at least `0.25`, the stored answer is shown; otherwise a safe fallback message asks the user to contact the college office.

This is a *retrieval-based* chatbot - it never makes up answers. All FAQ content is fictional/general and must be replaced with college-approved information before real use.

## Project files
| File | Purpose |
|---|---|
| `app.py` | Streamlit web interface |
| `chatbot.py` | NLP logic (preprocessing, TF-IDF, cosine similarity) |
| `faqs.csv` | FAQ dataset (question, answer, category) |
| `test_chatbot.py` | Tests the chatbot with different questions |
| `requirements.txt` | Python libraries needed |
| `screenshots/` | Screenshots of the application |

## Run on your computer (Windows)
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Open the link shown in the terminal (usually http://localhost:8501).

## Run the tests
```
python test_chatbot.py
```

## Update the answers
Open `faqs.csv` in Excel/Notepad, edit or add rows (`question,answer,category`), save, and restart the app.

## Limitations
- Matches words, not meaning - it may miss heavily reworded questions or spelling mistakes.
- Only knows what is in `faqs.csv`.
- Similarity score is a matching score, not a probability of being correct.

## Live demo
https://college-enquiry-chatbot-3fwg2zamf3vxu4t3epyacg.streamlit.app/
