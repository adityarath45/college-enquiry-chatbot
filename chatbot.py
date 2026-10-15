"""
chatbot.py - NLP logic for the College Enquiry Chatbot
Author: Aditya Rath

This file has NO Streamlit code. It only does:
1. Load the FAQ dataset (faqs.csv)
2. Clean the text (preprocessing)
3. Convert questions to numbers using TF-IDF
4. Find the most similar FAQ using Cosine Similarity
5. Return the answer, or a fallback message if nothing matches well
"""

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# If the best similarity score is below this number, we show the fallback.
# 0.25 is a starting value; we tuned it by testing different questions.
THRESHOLD = 0.25

FALLBACK_MESSAGE = (
    "Sorry, I could not find a verified answer to that question. "
    "Please contact the college office for help."
)


def preprocess(text):
    """Basic text cleaning: lowercase, remove punctuation, remove extra spaces."""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # keep only letters, digits, spaces
    text = re.sub(r"\s+", " ", text).strip()   # collapse multiple spaces
    return text


def load_faqs(path="faqs.csv"):
    """Read the CSV file and check that it has the needed columns."""
    df = pd.read_csv(path).fillna("")
    needed = {"question", "answer", "category"}
    if not needed.issubset(df.columns):
        raise ValueError("CSV must have the columns: question, answer, category")
    # remove rows where the question or answer is empty
    df = df[(df["question"].str.strip() != "") & (df["answer"].str.strip() != "")]
    return df.reset_index(drop=True)


class EnquiryBot:
    def __init__(self, path="faqs.csv"):
        self.faqs = load_faqs(path)
        if self.faqs.empty:
            raise ValueError("No valid FAQs found in the CSV file")
        # Clean every FAQ question once
        # We also add the category word (e.g. "Hostel") to help matching
        cleaned_questions = (self.faqs["question"] + " " + self.faqs["category"]).apply(preprocess)
        # TF-IDF: turns each question into a list of numbers
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.matrix = self.vectorizer.fit_transform(cleaned_questions)

    def get_answer(self, user_question):
        """Return (answer, category, score). category is None for the fallback."""
        cleaned = preprocess(user_question)
        if cleaned == "":
            return FALLBACK_MESSAGE, None, 0.0
        user_vector = self.vectorizer.transform([cleaned])
        # Cosine similarity: how close is the user's question to each FAQ question?
        scores = cosine_similarity(user_vector, self.matrix)[0]
        best = int(scores.argmax())
        best_score = float(scores[best])
        if best_score >= THRESHOLD:
            row = self.faqs.loc[best]
            return str(row["answer"]), str(row["category"]), best_score
        return FALLBACK_MESSAGE, None, best_score
