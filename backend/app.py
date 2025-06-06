# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="enclov-AI API", version="0.1.0")

# Input schema for prediction
class PredictRequest(BaseModel):
    data: str  # Change this to whatever your AI model expects

# Output schema for prediction response
class PredictResponse(BaseModel):
    prediction: str  # Adjust type and fields to your output

# Dummy model load (replace with your actual model loading)
def load_model():
    # Load your AI model here
    return "dummy-model"

model = load_model()

@app.get("/")
async def root():
    return {"message": "Welcome to enclov-AI API"}

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    # Replace this logic with your model inference code
    try:
        input_data = request.data
        # fake prediction example
        prediction = f"Predicted result for input: {input_data}"
        return PredictResponse(prediction=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
