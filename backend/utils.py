import pandas as pd
from io import BytesIO
import os

def read_excel(file_content: bytes, filename: str = None):
    try:
        ext = os.path.splitext(filename or "")[1].lower()
        sheets = {}

        if ext == ".csv":
            df = pd.read_csv(BytesIO(file_content))
            sheets["Sheet1"] = df
        else:
            xls = pd.ExcelFile(BytesIO(file_content))
            for sheet_name in xls.sheet_names:
                sheets[sheet_name] = xls.parse(sheet_name)

        return sheets

    except Exception as e:
        return {"error": str(e)}
