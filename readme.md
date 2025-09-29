# AI Data Agent

## Features

- Upload CSV or Excel files to the backend
- Ask questions about the uploaded data
- Dynamic handling of backend responses
- Safe file uploads with automatic directory creation
- Handles CORS for React + FastAPI

## Tech Stack

- **Frontend:** ReactJS, Axios
- **Backend:** FastAPI, Python 3.11+
- **Dependencies:** pandas (for CSV/Excel processing), uvicorn


## Backend Run

cd backend
pip install -r requirements.txt
uvicorn run:app --reload --host 127.0.0.1 --port 8000

## Frontend run
cd frontend
npm install 
npm run