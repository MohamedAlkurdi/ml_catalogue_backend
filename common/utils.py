import pandas as pd
import io

def preprocess_csv_string(csv_text: str) -> pd.DataFrame:
    """Common CSV preprocessing function"""
    df = pd.read_csv(io.StringIO(csv_text))
    if "id" in df.columns:
        df = df.drop("id", axis=1)
    df = df.replace({None: pd.NA})
    df = df.dropna()
    return df

def validate_csv_file(filename: str) -> bool:
    """Validate if file is a CSV"""
    return filename.lower().endswith('.csv')

def get_column_info(df: pd.DataFrame) -> List[dict]:
    """Get standardized column information"""
    return [{"name": col, "type": str(df[col].dtype)} for col in df.columns]