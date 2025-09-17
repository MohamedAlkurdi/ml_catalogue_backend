from fastapi import File, UploadFile, HTTPException, Body, APIRouter
import pandas as pd
import io
import numpy as np
from sklearn.decomposition import PCA

# Add the parent directory to Python path

from knn.utils.datalab import *
from knn.models.Point import *
from knn.models.Knn import *
from knn.functional_implementation.build_knn import *
from fastapi.middleware.cors import CORSMiddleware
from knn.api.api_utils import *

router = APIRouter()

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
