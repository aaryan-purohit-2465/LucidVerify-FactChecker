import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv("data/train_clean.csv")

# Adjust column names if needed
X = df["text"]
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_vec = vectorizer.fit_transform(X_train)

# Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Save artifacts
joblib.dump(model, "backend/app/baseline_model.pkl")
joblib.dump(vectorizer, "backend/app/tfidf_vectorizer.pkl")

print("✅ Baseline model and vectorizer saved")
