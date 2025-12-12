# LucidVerify – AI-Powered Fake News Detection & Fact-Checking System

LucidVerify is an AI-driven platform designed to detect fake news using 
a fine-tuned transformer model and validate facts by cross-verifying 
with trusted news sources in real time.

🚀 **Tech Stack (Planned)**
- Backend: FastAPI + Python
- Model: RoBERTa / DistilRoBERTa (HuggingFace Transformers)
- Frontend: React + Tailwind
- Deployment: Render (Backend) + Vercel (Frontend)

🗓 Deadline: **28th December 2025**
### Day 1 (4th Dec): Dataset collection and initial exploration completed.
### Day 2 (5th Dec)
- Cleaned Fake & True news datasets  
- Added binary labels (0 = Fake, 1 = True)  
- Merged datasets into a unified dataframe  
- Removed duplicates and missing values  
- Applied light text preprocessing  
- Created stratified Train / Validation / Test splits  
- Saved cleaned datasets for model training  
### Day 3 (6th Dec)
- Implemented TF-IDF + Logistic Regression baseline model  
- Achieved initial accuracy/F1 score on validation dataset  
- Saved model & vectorizer for backend integration  
### Day 4 (7th Dec)
- Set up DistilRoBERTa fine-tuning pipeline using HuggingFace Transformers.
- Converted cleaned news dataset into tokenized HuggingFace Datasets.
- Ran initial training/evaluation to validate the transformer-based approach.






