import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("backend/app/data/news.csv")

# Expecting columns: text, label
X = df["text"]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.7,
    ngram_range=(1, 2)
)

X_train_vec = vectorizer.fit_transform(X_train)

# Model
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Save model + vectorizer
with open("backend/app/ml_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("backend/app/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully.")
