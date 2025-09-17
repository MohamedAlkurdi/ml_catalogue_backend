from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

EXAMPLE_FILES_DIR = os.path.join(os.path.dirname(__file__), "../examples")

@router.get("/{filename}")
def get_example_file(filename: str):
    file_path = os.path.join(EXAMPLE_FILES_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}