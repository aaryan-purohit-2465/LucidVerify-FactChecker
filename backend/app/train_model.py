import pandas as pd
import joblib
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text


print("Loading dataset...")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

fake = pd.read_csv(os.path.join(DATA_DIR, "Fake.csv"))
true = pd.read_csv(os.path.join(DATA_DIR, "True.csv"))


fake["label"] = 0
true["label"] = 1

df = pd.concat([fake, true], axis=0)
df = df.sample(frac=1).reset_index(drop=True)

df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Vectorizing...")
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training model...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

print("Evaluating...")
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {acc:.4f}")

print("Saving model and vectorizer...")
joblib.dump(model, "model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")


print("Training complete.")
