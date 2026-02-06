@echo off
cd /d %~dp0

echo [INFO] Activating Virtual Environment...
if not exist ".venv" (
    echo [INFO] Creating .venv...
    python -m venv .venv
)
call .venv\Scripts\activate

echo [INFO] Installing Dependencies (if missing)...
pip install -r requirements.txt

echo [INFO] Starting FaceID Service (FastAPI)...
set API_KEY=SecureFaceIdKey2026
echo [INFO] API Key set to match appsettings.json
echo.
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
