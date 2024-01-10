# property-friends

Training pipeline and serving API for property valuation estimation.

### Requirements

- Docker >= 24.0.7

### Setup

First, download the `property_friends_config_files.zip` file provided in the email to Thamires Bengaly and extract it in the root of this repository.

Then, copy the files to the corresponding folders:

```
cd property_friends_config_files

cp pipeline.env ../training-pipeline/
cp api.env ../api/
cp bucket-writer.json ../training-pipeline/credentials/
cp bucket-reader.json ../api/credentials/

# These are the same datasets provided in the challenge
cp train.csv ../training-pipeline/data/
cp test.csv ../training-pipeline/data/
```

### Project structure

The project is divided in two parts, the training pipeline and the API. The main structure of the project is the following:

```bash
.
├── api
│   ├── api.env                 # API environment variables
│   ├── app                     # FastAPI app
│   │   ├── auth.py                 # Authentication with API Key
│   │   ├── config.py               # Configuration that loads environment variables
│   │   ├── logger.py               # Logging configuration
│   │   ├── main.py                 # Main file that runs the application
│   │   ├── middleware.py           # Middleware that logs each request to the API
│   │   ├── utils.py                # Utility functions to load the model
│   │   └── schema.py               # Pydantic schema for the data to predict
│   ├── credentials             # Credentials to access the GCS bucket
│   ├── Dockerfile              # Dockerfile to build the API
│   ├── logs                    # Logs of the API
│   ├── models                  # Loaded models
│   ├── Pipfile                 # Dependencies
│   ├── Pipfile.lock
│   └── pyproject.toml          # Project configuration
└── training-pipeline
    ├── credentials             # Credentials to access the GCS bucket
    ├── data                    # Data to train and evaluate the model
    ├── Dockerfile              # Dockerfile to build the training pipeline
    ├── models                  # Trained models
    ├── pipeline.env            # Pipeline environment variables
    ├── Pipfile                 # Dependencies
    ├── Pipfile.lock
    ├── pyproject.toml          # Project configuration
    └── src
        ├── config.py           # Configuration that loads environment variables
        ├── dataloader.py       # Dataloader that builds the datasets
        ├── train.py            # Training script
        └── utils.py            # Utility functions
```

## 1. Training pipeline

The training pipeline is located in the `training-pipeline` folder.

### Asumptions

- The Client is happy with the results of the current model, so further hyperparameter tuning or model selection is not currently covered in this pipeline.

Suggestions for improvement are [here](#suggestions-for-improvement).

### Instructions

First, build the Docker image. In a terminal, run:

```
cd training-pipeline
docker build -t training-pipeline:latest .
```

Then, run the pipeline with Docker:

```
docker run training-pipeline:latest
```

It will train the model and you should get these test metrics of the trained model:

```
RMSE:  10254.155686652393
MAPE:  0.40042979298798137
MAE :  5859.374796053153
```

## 2. Property valuation estimation API

This is an API to estimate the valuation of a property in Chile.

### Asumptions

Suggestions for improvement are [here](#suggestions-for-improvement).

### Instructions

Same as above, first build the Docker image, and then run the API with Docker.

```
docker build -t api:latest .
docker run -p 8000:8000 api:latest
```

To execute a prediction, there are two options:

##### Test in the terminal with `curl`

In another terminal, run

```
curl -i -X POST "http://0.0.0.0:8000/predict" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-H "X-API-Key: <THE_API_KEY>" \
-d '<THE_DATA>'
```

where `<THE_API_KEY>` is the API Key provided in the email to Thamires Bengaly, and `<THE_DATA>` is the data to predict. For example: `{"type": "casa", "sector": "la reina", "net_usable_area": 50, "net_area": 70, "n_rooms": 3, "n_bathroom": 2, "latitude": -70, "longitude": -80}`.

##### Test with browser

In a browser, open `0.0.0.0/docs`, Authenticate with the API Key and test the method `predict` by clicking on `Try it out` and filling the data to predict.

## Suggestions for improvement
