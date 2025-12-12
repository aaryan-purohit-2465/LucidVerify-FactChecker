# notebooks/check_and_recreate_baseline.py
import os, pickle, joblib
p1 = os.path.join("backend","app","baseline_model.pkl")
p2 = os.path.join("backend","app","tfidf_vectorizer.pkl")

print("exists baseline:", os.path.exists(p1))
print("exists vectorizer:", os.path.exists(p2))

def try_load_pickle(p):
    try:
        with open(p,'rb') as f:
            obj = pickle.load(f)
        print(p, "loaded OK, type:", type(obj))
        return True
    except Exception as e:
        print("FAILED to load", p, repr(e))
        return False

try_load_pickle(p1)
try_load_pickle(p2)

# -- if they fail, here's how to recreate a simple baseline (quick demo)
if not (os.path.exists(p1) and os.path.exists(p2)):
    print("Recreating small baseline model using train_clean.csv sample")
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    data_path = os.path.join("data","train_clean.csv")  # adjust name if different
    if not os.path.exists(data_path):
        print("no train CSV found at", data_path)
    else:
        df = pd.read_csv(data_path)
        # adjust column names to your dataset
        text_col = "text" if "text" in df.columns else df.columns[0]
        label_col = "label" if "label" in df.columns else df.columns[1]
        X = df[text_col].astype(str)
        y = df[label_col]
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        vectorizer = TfidfVectorizer(max_features=10000, stop_words="english", ngram_range=(1,2))
        X_train_t = vectorizer.fit_transform(X_train)
        model = LogisticRegression(C=2, max_iter=2000, class_weight="balanced")
        model.fit(X_train_t, y_train)

        # save with joblib = more robust for big arrays
        joblib.dump(model, p1)
        joblib.dump(vectorizer, p2)
        print("Saved baseline model and vectorizer:", p1, p2)
