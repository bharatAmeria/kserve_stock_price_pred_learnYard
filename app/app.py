import numpy as np

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
from joblib import load

model = load("model.pkl")


# Initialize FastAPI app
app = FastAPI()

# Preprocessor
sclr = StandardScaler()

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

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
