from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import re
import os
from votes import context_vote, textblob_vote, subjectivity_vote, profanity_vote, intensity_vote

app = FastAPI()

# Load processors
count_vectorizer = joblib.load("vectorizer/count_vectorizer.pkl")
tfidf_transformer = joblib.load("vectorizer/tfidf_transformer.pkl")

# Load ML models
models = {
    1: {"name": "SVM", "model": joblib.load("models/svm_hate_speech_model.pkl")},
    2: {"name": "XGBoost", "model": joblib.load("models/xgb_hsd_model.pkl")},
    3: {"name": "Logistic Regression", "model": joblib.load("models/logistic_regression_hsd_model.pkl")},
    4: {"name": "Naive Bayes", "model": joblib.load("models/naive_bayes_hsd_model.pkl")},
}

class InputData(BaseModel):
    text: str

def preprocess(text):
    text = text.lower()
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'[^0-9A-Za-z \t]', ' ', text)
    text = " ".join(text.split())
    return text

@app.get("/")
def read_root():
    return {"message": "Hate Speech Detection API is running."}

@app.get("/models")
def get_models():
    return {k: v["name"] for k, v in models.items()}

@app.post("/predict_ensemble")
def predict_ensemble(data: InputData):
    text = preprocess(data.text)

    # Vectorization
    count_vec = count_vectorizer.transform([text])
    tfidf_vec = tfidf_transformer.transform(count_vec)

    votes = []

    # ML model votes
    for model_id, model_info in models.items():
        prediction = model_info["model"].predict(tfidf_vec)[0]
        label = "hate_speech" if prediction == 1 else "not_hate_speech"
        votes.append(label)

    # Heuristic rule votes
    votes.append(context_vote(data.text))
    votes.append(textblob_vote(data.text))
    votes.append(subjectivity_vote(data.text))
    votes.append(profanity_vote(data.text))
    votes.append(intensity_vote(data.text))

    hate_votes = votes.count("hate_speech")
    not_hate_votes = votes.count("not_hate_speech")

    final_prediction = "Hate Speech" if hate_votes > not_hate_votes else "Not Hate Speech"

    return {
        "votes": votes,
        "hate_votes": hate_votes,
        "not_hate_votes": not_hate_votes,
        "final_prediction": final_prediction
    }
