class JobStore:
    
    def __init__(self):
        self.jobs = {}
    
    def create_job(self, job_id: str, filename: str, file_path: str):
        self.jobs[job_id] = {
            "job_id": job_id,
            "original_filename": filename,
            "file_path": file_path,
            "status": "processing",
            "progress": 0,
            "algorithm_used": None,
            "output_file": None,
            "error": None
        }
    
    def get_job(self, job_id: str):
        return self.jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs):
        if job_id in self.jobs:
            self.jobs[job_id].update(kwargs)

job_store = JobStore()
