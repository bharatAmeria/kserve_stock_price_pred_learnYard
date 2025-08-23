import numpy as np
import boto3
import joblib
import tempfile
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# S3 configuration from environment variables
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
MODEL_KEY = os.getenv("MODEL_S3_KEY", "models/model.pkl")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Validate required environment variables
if not S3_BUCKET_NAME:
    raise ValueError("S3_BUCKET_NAME environment variable is required")

# Initialize S3 client (will automatically use environment variables)
s3_client = boto3.client('s3', region_name=AWS_REGION)

# Function to load model from S3
def load_model_from_s3():
    try:
        # Create a temporary file to store the downloaded model
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as temp_file:
            # Download model from S3
            s3_client.download_file(S3_BUCKET_NAME, MODEL_KEY, temp_file.name)
            # Load the model using joblib
            model = joblib.load(temp_file.name)
            # Clean up temporary file
            os.unlink(temp_file.name)
            return model
    except Exception as e:
        print(f"Error loading model from S3: {e}")
        raise

# Load model from S3
model = load_model_from_s3()

# model = joblib.load("model.pkl")

# Preprocessor
sclr = StandardScaler()

# Set up Jinja2 templates directory
import os
template_dir = "templates" if os.path.exists("templates") else "../templates"
templates = Jinja2Templates(directory=template_dir)

# Root GET endpoint
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# POST prediction endpoint
@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    Open: float = Form(...),
    High: float = Form(...),
    Low: float = Form(...),
    Adj_Close: float = Form(...),
    Volume: float = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    day: int = Form(...)
):
    # Combine features
    features = np.array([[Open, High, Low, Adj_Close, Volume, year, month, day]])
    features = sclr.fit_transform(features)  # Ideally use same scaler as training
    prediction = model.predict(features)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "output": prediction[0]
    })

# Optional: Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

# KServe compatible endpoints
@app.get("/v1/models/fastapi-serve")
async def model_metadata():
    return {
        "name": "fastapi-serve",
        "versions": ["v1"],
        "platform": "sklearn",
        "inputs": [
            {"name": "Open", "datatype": "FP32", "shape": [1]},
            {"name": "High", "datatype": "FP32", "shape": [1]},
            {"name": "Low", "datatype": "FP32", "shape": [1]},
            {"name": "Adj_Close", "datatype": "FP32", "shape": [1]},
            {"name": "Volume", "datatype": "FP32", "shape": [1]},
            {"name": "year", "datatype": "INT32", "shape": [1]},
            {"name": "month", "datatype": "INT32", "shape": [1]},
            {"name": "day", "datatype": "INT32", "shape": [1]}
        ],
        "outputs": [
            {"name": "prediction", "datatype": "FP32", "shape": [1]}
        ]
    }

@app.post("/v1/models/fastapi-serve:predict")
async def kserve_predict(request: Request):
    """KServe compatible prediction endpoint"""
    try:
        body = await request.json()
        inputs = body.get("inputs", [])
        
        if len(inputs) != 8:
            return {"error": "Expected 8 input values"}
        
        # Extract values assuming they're in the correct order
        features = np.array([inputs])
        features = sclr.fit_transform(features)
        prediction = model.predict(features)
        
        return {
            "model_name": "fastapi-serve",
            "model_version": "v1",
            "outputs": [
                {
                    "name": "prediction",
                    "datatype": "FP32",
                    "shape": [1],
                    "data": [float(prediction[0])]
                }
            ]
        }
    except Exception as e:
        return {"error": str(e)}

# Alternative KServe prediction endpoint with better input handling
@app.post("/v1/models/fastapi-serve/infer")
async def kserve_infer(request: Request):
    """Alternative KServe inference endpoint"""
    try:
        body = await request.json()
        
        # Handle both array input and named inputs
        if "inputs" in body:
            if isinstance(body["inputs"], list) and len(body["inputs"]) == 8:
                inputs = body["inputs"]
            elif isinstance(body["inputs"], dict):
                # Extract from named inputs
                inputs = [
                    body["inputs"].get("Open", 0),
                    body["inputs"].get("High", 0),
                    body["inputs"].get("Low", 0),
                    body["inputs"].get("Adj_Close", 0),
                    body["inputs"].get("Volume", 0),
                    body["inputs"].get("year", 2024),
                    body["inputs"].get("month", 1),
                    body["inputs"].get("day", 1)
                ]
            else:
                return {"error": "Invalid input format"}
        else:
            return {"error": "Missing 'inputs' field"}
        
        features = np.array([inputs])
        features = sclr.fit_transform(features)
        prediction = model.predict(features)
        
        return {
            "model_name": "fastapi-serve",
            "model_version": "v1",
            "id": "prediction-001",
            "outputs": [
                {
                    "name": "prediction",
                    "datatype": "FP32",
                    "shape": [1],
                    "data": [float(prediction[0])]
                }
            ]
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}


