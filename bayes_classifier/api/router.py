from fastapi import FastAPI, File, UploadFile, HTTPException, Body, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import pandas as pd
import io
from typing import Any, Dict

# algorithm functions is in this package
from bayes_classifier.logic.algorithm import calculate_probs, classify

router = APIRouter()


def _preprocess_csv_string(csv_text: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(csv_text))
    if "id" in df.columns:
        df = df.drop("id", axis=1)
    df = df.replace({None: pd.NA})
    df = df.dropna()
    return df


@router.get("/")
def index():
    return {"message": "bayes_classifier service running"}


@router.post("/preview-csv")
async def preview_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")
    try:
        content = await file.read()
        text = content.decode("utf-8")
        df = _preprocess_csv_string(text)
        
        if df.shape[0] == 0:  # Check if the DataFrame has zero rows
            raise HTTPException(status_code=400, detail="Uploaded file contains no data")
        
        preview = df.to_dict(orient="records")
        columns = [{"name": col, "type": str(df[col].dtype)} for col in df.columns]
        
        return {"preview": preview, "columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


@router.post("/process-csv")
async def process_csv(
    file_content: str = Body(..., embed=True),
    target_index: int = Body(-1, embed=True),
    test_point: Dict[str, Any] = Body(..., embed=True),
):
    try:
        df = _preprocess_csv_string(file_content)

        probs = calculate_probs(test_point, df, target_index)
        classification = classify(probs)

        payload = {
            "operation_type": "naive_bayes",
            "result": {"probs": probs, "classification": classification},
        }
        # make sure all numpy/pandas types are converted to plain json types
        return jsonable_encoder(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running classifier: {e}")