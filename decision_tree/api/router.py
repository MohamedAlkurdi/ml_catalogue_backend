from fastapi import File, UploadFile, HTTPException, Body, APIRouter
from decision_tree.functional_implementation.functional_decision_tree import *
import pandas as pd
import numpy as np
import io

router = APIRouter()


def preprocess_data(file_content):
    data = pd.read_csv(io.StringIO(file_content))
    if "id" in data.columns:
        data = data.drop('id', axis=1)
    data = data.replace({None: np.nan})
    data = data.dropna()
    return data

@router.get("/")
def index():
    return {"message":"yea boiiiii decision tree"}

@router.post("/data_preview")
async def preview_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")
    try:
        content = await file.read()
        data = pd.read_csv(io.StringIO(content.decode('utf-8')))
        if "id" in data.columns:
            data = data.drop('id', axis=1)
        data = data.replace({None: np.nan})
        data = data.dropna()
        preview = data.to_dict(orient="records")
        columns = [{"name": col, "type": str(data[col].dtype)} for col in data.columns]
        
        return {
            "preview": preview,
            "columns": columns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
@router.post("/data_process")
async def process_csv(
    file_content: str = Body(..., embed=True),
    target_index: int = Body(-1, embed=True)
    ):
    try:
        data = preprocess_data(file_content)
        decision_tree = build_tree(data, {}, target_index)
        return {
            "decision_tree": decision_tree
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

