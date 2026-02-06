# FaceID Microservice (Python)

This is the standalone AI service for the Swann Jewelry FaceID system.
It uses **FastAPI** + **DeepFace (ArcFace)** to provide face embedding extraction.

## Features
- **API Key Security**: Requires `X-API-Key` header.
- **Health Check**: `GET /ping`.
- **Face Extraction**: `POST /extract`.

## Local Development
1. Create venv: `python -m venv .venv`
2. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn main:app --reload`

## Cloud Deployment (Render/Railway)
This folder is ready to be deployed as a standalone repo.

1. **Environment Variables**:
   - `API_KEY`: Your secret key (must match ASP.NET Core `appsettings.json`).
   - `TF_USE_LEGACY_KERAS`: Set to `1`.
   - `PORT`: (Managed by host, usually does not need manual setting on Render).

## Endpoints

### 1. Health Check
- **URL**: `/ping`
- **Method**: `GET`
- **Response**: `{"status": "ok", "service": "FaceID API"}`

### 2. Extract Embedding
- **URL**: `/extract`
- **Method**: `POST`
- **Headers**: `X-API-Key: <YOUR_KEY>`
- **Body**:
  ```json
  {
    "image": "base64_encoded_string..."
  }
  ```
- **Response**: `{"embedding": [0.123, -0.456, ...]}`
