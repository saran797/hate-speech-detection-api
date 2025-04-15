from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os


app = FastAPI()

SUPPORTED_MODELS = {
    1: {"file": "logistic_regression_hsd_model.pkl", "name": "Logistic Regression Model"},
    2: {"file": "naive_bayes_hsd_model.pkl", "name": "Navie Bayes Model"},
    3: {"file": "svm_hate_speech_model.pkl", "name": "Svm Model"},
    4: {"file": "xgb_hsd_model.pkl", "name": "XgBoost Model"}
}

# Load vectorizers (CountVectorizer, TfidfTransformer)
try:
    with open("vectorizers/count_vectorizer.pkl", "rb") as f:
        count_vectorizer = pickle.load(f)
    with open("vectorizers/tfidf_transformer.pkl", "rb") as f:
        tfidf_transformer = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load vectorizers: {e}")

# Define the request body schema
class PredictionRequest(BaseModel):
    model_id: int  # Model ID as an integer
    text: str      # The text for prediction

# Function to load the selected model
def load_model(model_id):
    # Ensure the model ID is valid
    if model_id not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model ID: {model_id}")
    
    # Define the path to the model file
    path = f"models/{SUPPORTED_MODELS[model_id]['file']}"
    
    # Check if the model file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    
    # Load and return the model
    with open(path, "rb") as f:
        return pickle.load(f)

# Prediction endpoint
@app.post("/predict")
def predict(req: PredictionRequest):
    try:
        # Load the model based on the model ID provided
        model = load_model(req.model_id)
        
        # Vectorize the input text
        count_features = count_vectorizer.transform([req.text])
        tfidf_features = tfidf_transformer.transform(count_features)
        
        # Make the prediction
        prediction = model.predict(tfidf_features)[0]
        
        # Return the prediction as a JSON response
        return {
            "model_id": req.model_id,
            "is_hateful": int(prediction)  # Convert prediction to an integer (0 or 1)
        }
    
    except Exception as e:
        # Return error message if any exception occurs
        return {"error": str(e)}

# Endpoint to get the available models with both IDs and names
@app.get("/models")
def list_models():
    # Return the model IDs and their names in a structured format
    model_info = [{"model_id": model_id, "model_name": model_info["name"]} 
                  for model_id, model_info in SUPPORTED_MODELS.items()]
    return {"available_models": model_info}
