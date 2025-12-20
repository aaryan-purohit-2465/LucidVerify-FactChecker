import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load data
df_true = pd.read_csv("data/True.csv")
df_fake = pd.read_csv("data/Fake.csv")

df_true["label"] = 1
df_fake["label"] = 0

df = pd.concat([df_true, df_fake], ignore_index=True)
df = df.sample(frac=1).reset_index(drop=True)

X = df["text"]
y = df["label"]

# Vectorizer
vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english"
)

X_vec = vectorizer.fit_transform(X)

# Model
model = LogisticRegression(max_iter=2000)
model.fit(X_vec, y)

# Save
joblib.dump(model, "backend/app/model.joblib")
joblib.dump(vectorizer, "backend/app/vectorizer.joblib")

print("✅ Model and vectorizer saved")
