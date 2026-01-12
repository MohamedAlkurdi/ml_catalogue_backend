from fastapi import File, UploadFile, HTTPException, Body, APIRouter
import pandas as pd
import io
import numpy as np
import requests

from knn.utils.datalab import *
from knn.models.Point import *
from knn.models.Knn import *
from knn.functional_implementation.build_knn import *
from fastapi.middleware.cors import CORSMiddleware
from knn.api.api_utils import *
from models.job import job_store
import logging 

logger = logging.getLogger(__name__)

router = APIRouter()

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    first_row = pd.Series(df.columns)
    second_row = df.iloc[1]
    types_match = sum(type(v1).__name__ == type(v2).__name__ for v1, v2 in zip(first_row, second_row))
    are_all_match=  len(first_row) == types_match
    if are_all_match:
        df.columns = [f"column_{i+1}" for i in range(len(df.columns))]
        print(r"no header detected, generated column names (column_{i}))")

    elif isinstance(df.columns, pd.RangeIndex):
        df.columns = [f"column_{i+1}" for i in range(len(df.columns))]
        print("index-alike header detected, replaced with generic column names.")

    else:
        print("header detected, kept the original column names.")

    df = df.replace([pd.NA, pd.NaT, float("inf"), float("-inf"), np.inf, -np.inf], None)
    df = df.where(pd.notna(df), None)
    df = df.dropna()

    for col in df.select_dtypes(include=["object"]):
        try:
            numeric_col = pd.to_numeric(df[col])
            df[col] = numeric_col
        except (ValueError, TypeError):
            pass
    return df

# def run_job(job_id: str, file_path: str, filename: str):
#     logger.info(f"Job {job_id} started in background")
    
#     try:
#         job_store.update_job(job_id, status="processing", progress=5)
        
#         if filename.endswith('.parquet'):
#             data = prepare_data(pd.read_parquet(file_path))
#         elif filename.endswith(".xls") or filename.endswith(".xlsx"):
#             data = prepare_data(pd.read_excel(file_path))
#         else:
#             data = prepare_data(pd.read_csv(file_path))
        
#         payload = {
#             "file_df": data.to_dict(orient='records'),
#             "original_filename": filename,
#         }
        
#         # Update job store with results
#         job_store.update_job(
#             job_id,
#             status="completed",
#             progress=100,
#             output_file=output_file,
#             algorithm_used=result["model_used"],
#         )
        
#         logger.info(f"Job {job_id} completed successfully")
        
#     except requests.exceptions.Timeout:
#         error_msg = "ML service request timed out"
#         logger.error(f"Job {job_id}: {error_msg}")
#         job_store.update_job(job_id, status="failed", error=error_msg)
        
#     except requests.exceptions.ConnectionError as e:
#         error_msg = f"Failed to connect to ML service: {str(e)}"
#         logger.error(f"Job {job_id}: {error_msg}")
#         job_store.update_job(job_id, status="failed", error=error_msg)
        
#     except requests.exceptions.RequestException as e:
#         error_msg = f"Request error: {str(e)}"
#         logger.error(f"Job {job_id}: {error_msg}")
#         job_store.update_job(job_id, status="failed", error=error_msg)
        
#     except Exception as e:
#         error_msg = f"Unexpected error: {str(e)}"
#         logger.error(f"Job {job_id}: {error_msg}", exc_info=True)
#         job_store.update_job(job_id, status="failed", error=error_msg)


@router.get("/")
def index():
    return {"message": "yea boiiiii"}


@router.post("/preview-csv/")
async def preview_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")
    try:
        content = await file.read()
        data = pd.read_csv(io.StringIO(content.decode("utf-8")))
        if "id" in data.columns:
            data = data.drop("id", axis=1)
        data = data.replace({None: np.nan})
        data = data.dropna()
        # preview = data.head(5).to_dict(orient="records")
        preview = data.to_dict(orient="records")
        columns = [{"name": col, "type": str(data[col].dtype)} for col in data.columns]

        return {"preview": preview, "columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/process-csv/")
async def process_csv(
    file_content: str = Body(..., embed=True),
    target_index: int = Body(-1, embed=True),
    test_point: dict = Body(..., embed=True),
):
    try:
        # load and split data
        data = preprocess_data(file_content)
        target = extract_target_column(data, target_index)
        features = data.drop(data.columns[target_index], axis=1)

        # prepare test point as single-row dataframe and align dtypes
        test_point_df = pd.DataFrame([preprocess_test_point(test_point, features)])
        features = ensure_str_categoricals(features)
        test_point_df = ensure_str_categoricals(test_point_df)

        # one-hot encode and align columns between train and test
        features = pd.get_dummies(features)
        test_point_encoded = pd.get_dummies(test_point_df).reindex(
            columns=features.columns, fill_value=0
        )

        # scale training features, attach target and find best K
        scaler = StandardScaler()
        scaled_train = scaler.fit_transform(features)
        data_scaled = pd.DataFrame(scaled_train, columns=features.columns)
        data_scaled["target"] = target.reset_index(drop=True)
        best_k = evaluate(data_scaled)

        # scale test point, build Point (unknown target) and predict
        sample_vals = scaler.transform(test_point_encoded)[0].tolist()
        test_pt = Point(*sample_vals, target=None)
        prediction = predict(test_pt, data_scaled, best_k)

        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
