from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import re
import os

app = FastAPI()

# Load processors
count_vectorizer = joblib.load("vectorizer/count_vectorizer.pkl")
tfidf_transformer = joblib.load("vectorizer/tfidf_transformer.pkl")

# Load models
models = {
    1: {"name": "SVM", "model": joblib.load("models/svm_hate_speech_model.pkl")},
    2: {"name": "XGBoost", "model": joblib.load("models/xgb_hsd_model.pkl")},
    3: {"name": "Logistic Regression", "model": joblib.load("models/logistic_regression_hsd_model.pkl")},
    4: {"name": "Naive Bayes", "model": joblib.load("models/naive_bayes_hsd_model.pkl")},
}

class InputData(BaseModel):
    text: str
    model_id: int

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

@app.post("/predict")
def predict(data: InputData):
    if data.model_id not in models:
        return {"error": "Invalid model ID"}

    model = models[data.model_id]["model"]
    text = preprocess(data.text)

    count_vec = count_vectorizer.transform([text])
    tfidf_vec = tfidf_transformer.transform(count_vec)

    prediction = model.predict(tfidf_vec)[0]
    result = "Hate Speech" if prediction == 1 else "Not Hate Speech"
    return {
        "model": models[data.model_id]["name"],
        "prediction": result
    }
