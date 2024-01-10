import pandas as pd
import uvicorn
from fastapi import FastAPI, Security
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import get_valid_api_key
from .config import settings
from .middleware import log_middleware
from .model_utils import load_model_from_gcs
from .schema import Property

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

model = load_model_from_gcs()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Hello World"}


@app.post("/predict")
def predict(
    property: Property, api_key: str = Security(get_valid_api_key)
) -> dict[str, float]:
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
