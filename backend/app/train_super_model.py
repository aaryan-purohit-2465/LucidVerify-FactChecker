import pandas as pd
import joblib
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

print("Loading dataset...")

fake = pd.read_csv("../../data/Fake.csv")
true = pd.read_csv("../../data/True.csv")


fake["label"] = 0
true["label"] = 1

df = pd.concat([fake, true])
df = df.sample(frac=1).reset_index(drop=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

print("Cleaning text...")
df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Training model...")

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_df=0.7)),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

print("Evaluating...")
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("Model Accuracy:", acc)

print("Saving model...")
joblib.dump(model, "super_model.joblib")

print("Training complete!")
