from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from google import genai
import os
from utils import read_excel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store the last uploaded file path in memory
last_uploaded_file_path = None

@app.post("/upload")
async def upload_file(file: UploadFile):
    global last_uploaded_file_path
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        content = await file.read()

        # Save locally
        with open(file_path, "wb") as f:
            f.write(content)

        # Remember this file
        last_uploaded_file_path = file_path

        # Read Excel/CSV
        sheets = read_excel(content, file.filename)
        if "error" in sheets:
            return JSONResponse(status_code=400, content={"error": sheets["error"]})

        return {"status": "success", "sheets": list(sheets.keys())}

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    global last_uploaded_file_path
    try:
        if not last_uploaded_file_path or not os.path.exists(last_uploaded_file_path):
            return JSONResponse(status_code=404, content={"error": "No uploaded file found. Please upload first."})

        with open(last_uploaded_file_path, "rb") as f:
            content = f.read()

        sheets = read_excel(content, os.path.basename(last_uploaded_file_path))
        if "error" in sheets:
            return JSONResponse(status_code=400, content={"error": sheets["error"]})

        # Prepare prompt for Gemini
        data_preview = ""
        for sheet, df in sheets.items():
            data_preview += f"Sheet: {sheet}\n{df.head().to_csv()}\n"

        prompt = f"""
        You are a data analyst. Answer the following question based on the provided data:

        {data_preview}

        Question: {question}

        Answer with explanation and any charts in text form if possible.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text.strip()
        return {"answer": answer}

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
