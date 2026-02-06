import os
import uvicorn
import numpy as np
import base64
import cv2
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from deepface import DeepFace
from starlette.middleware.cors import CORSMiddleware

# --- Configuration ---
API_KEY = os.getenv("API_KEY", "DefaultSecretKey_ChangeMe")
PORT = int(os.getenv("PORT", 5000))

app = FastAPI(title="FaceID Microservice", version="1.0")

# CORS (Allow all for flexibility in PaaS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency: Validate API Key ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# --- Data Models ---
class ImageRequest(BaseModel):
    image: str  # Base64 string

# --- Helper Logic ---
def decode_base64_image(base64_string):
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

# --- Endpoints ---

@app.get("/ping")
def health_check():
    """Simple health check endpoint for uptime monitors."""
    return {"status": "ok", "service": "FaceID API"}

@app.post("/extract", dependencies=[Depends(verify_api_key)])
def extract_embedding(req: ImageRequest):
    """
    Extracts face embedding from a base64 image.
    Returns a list of floats (vector).
    """
    try:
        # 1. Decode Image
        img = decode_base64_image(req.image)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        # 2. Extract Embedding (ArcFace)
        # enforce_detection=True ensures we only process valid faces
        embedding_objs = DeepFace.represent(
            img_path=img,
            model_name="ArcFace",
            enforce_detection=True,
            detector_backend="mtcnn" 
        )

        if not embedding_objs:
             raise HTTPException(status_code=400, detail="No face detected")

        # 3. Return the first face's embedding
        embedding = embedding_objs[0]["embedding"]
        return {"embedding": embedding}

    except ValueError as e:
        # DeepFace raises ValueError if face not found (when enforce_detection=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
