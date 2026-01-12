import sys
import os
from fastapi.responses import FileResponse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bayes_classifier.api.router import router as bayes_router
from knn.api.router import router as knn_router  
from decision_tree.api.router import router as dt_router

from common.middleware import add_logging_middleware
from common.config import settings
import logging 

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.api_title,
    description="Unified ML Algorithms API with modular architecture",
    version="1.0.0",
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_logging_middleware(app)

app.include_router(bayes_router, prefix="/bayes", tags=["Bayes Classifier"])
app.include_router(knn_router, prefix="/knn", tags=["K-Nearest Neighbors"])
app.include_router(dt_router, prefix="/dt", tags=["Decision Tree"])

@app.get("/")
def root():
    return {
        "message": "Unified ML Algorithms API",
        "algorithms": ["bayes_classifier", "knn", "decision_tree"],
        "endpoints": {
            "bayes_classifier": ["/bayes", "/bayes/preview-csv", "/bayes/process-csv"],
            "knn": ["/knn", "/knn/preview-csv", "/knn/process-csv"],
            "decision_tree": ["/dt", "/dt/preview-csv", "/dt/process-csv"]
        }
    }
    
@app.get("/demo")
def get_demo_file():
    file_path = '../examples/example.csv'
    logger.info("entered get_demo_file function")
    if os.path.exists(file_path):
        logger.info("from get_demo_file: path does not exist")
        return FileResponse(file_path)
    logger.info("from get_demo_file: path exists")
    return {"error": "File not found"}