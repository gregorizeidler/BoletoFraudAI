from fastapi import FastAPI, UploadFile, File
from app.services import analyze_boleto
import cv2
import numpy as np

app = FastAPI(title="BoletoFraudAI", description="AI-powered fake boleto detector")

@app.get("/")
def root():
    return {"message": "BoletoFraudAI - Fake Boleto Detector API"}

@app.post("/detect/")
async def detect_fraud(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    result = analyze_boleto(image)
    return {"fraud_detected": result["fraud_detected"], "message": result["message"]}
