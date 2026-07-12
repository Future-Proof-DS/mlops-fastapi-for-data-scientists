"""The FastAPI service that serves our churn model.

Run it with:

    uvicorn my_ml_project.api:app --reload

Then open http://localhost:8000/docs to try it out.
"""

import logging
from pathlib import Path

import joblib
from fastapi import FastAPI

from my_ml_project.schemas import PredictionRequest, PredictionResponse

# Configure logging once, here, so every prediction shows up in your terminal.
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Churn Prediction Service")

# Load the model ONCE at import time, not on every request. Loading from disk
# is slow, so we pay that cost a single time when the server starts up.
# parents[2] walks up from src/my_ml_project/api.py to the project root.
MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "churn_model.pkl"
model = joblib.load(MODEL_PATH)


def to_risk_band(probability: float) -> str:
    """Turn a raw probability into a label a human can act on."""
    if probability < 0.33:
        return "low"
    if probability < 0.66:
        return "medium"
    return "high"


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Predict churn probability for a single customer."""
    # The model expects features in the same order they were trained on.
    features = [[request.age, request.income, request.tenure_months]]

    # predict_proba returns [[P(stay), P(churn)]]; we want the churn column.
    probability = float(model.predict_proba(features)[0][1])
    risk_band = to_risk_band(probability)

    logger.info(
        "Prediction made | age=%s income=%s tenure_months=%s -> probability=%.3f band=%s",
        request.age,
        request.income,
        request.tenure_months,
        probability,
        risk_band,
    )

    return PredictionResponse(churn_probability=probability, risk_band=risk_band)


# TODO: Implement a health check endpoint.
# It should:
#   - Respond to GET requests at /health
#   - Return a JSON response like {"status": "ok"}
# This is what infrastructure tools use to know your service is alive.
#
# See the README for hints if you get stuck.
