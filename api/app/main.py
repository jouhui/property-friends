from typing import Literal

import pandas as pd
import uvicorn
from fastapi import FastAPI, Security
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import get_valid_api_key
from .config import settings
from .middleware import log_middleware
from .utils import load_model_from_gcs

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

try:
    model = load_model_from_gcs()
except Exception as e:
    raise RuntimeError("Error loading the model from GCS") from e


class Property(BaseModel):
    """Entity to represent a property."""

    type: Literal["casa", "departamento"]
    sector: Literal[
        "la reina",
        "las condes",
        "vitacura",
        "lo barnechea",
        "nunoa",
        "providencia",
        "vitacura",
    ]
    net_usable_area: float
    net_area: float
    n_rooms: int
    n_bathroom: int
    latitude: float
    longitude: float


class Prediction(BaseModel):
    """Entity to represent a property prediction."""

    prediction: float


@app.get("/")
def home(api_key: str = Security(get_valid_api_key)) -> dict[str, str]:
    """Home endpoint. The API Key must be provided in the request header.

    Raises:
        401 Unauthorized: If the API Key is invalid.
    """
    return {"message": "This is the API for the property price prediction model."}


@app.get("/health")
def health(api_key: str = Security(get_valid_api_key)) -> dict[str, str]:
    """Health check endpoint. The API Key must be provided in the request header.

    Raises:
        401 Unauthorized: If the API Key is invalid.
    """
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(property: Property, api_key: str = Security(get_valid_api_key)) -> dict[str, float]:
    """Endpoint to make predictions given a property. The API Key must be provided in the
    request header.

    Args:
        property (Property): The property to make the prediction.
        api_key (str, optional): API Key for authentication.

    Raises:
        401 Unauthorized: If the API Key is invalid.

    Returns:
        dict[str, float]: A dictionary with the predicted property price.
    """
    data = pd.DataFrame(property.model_dump(), index=[0])
    prediction = model.predict(data)[0]
    return {"prediction": prediction}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
