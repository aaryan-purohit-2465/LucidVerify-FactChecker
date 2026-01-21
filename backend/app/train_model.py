import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/news.csv")

# Expect columns: text,label   (label: fake=0, real=1)
df = df.dropna()

X = df["text"]
y = df["label"]

# Vectorizer
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vec, y)

# Test
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2)
acc = model.score(X_test, y_test)

print("Accuracy:", acc)

# Save
joblib.dump(model, "ml_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Model and vectorizer saved.")
