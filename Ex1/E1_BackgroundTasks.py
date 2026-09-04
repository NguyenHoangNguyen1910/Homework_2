from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time 

app = FastAPI()


class InferRequest(BaseModel):
    text: str
    
def worker(text: str):
    print("Bat dau lam viec")
    time.sleep(10)
    new_text = text.upper()
    print("Da xu ly xong:", new_text)
    
    
@app.post("/job")
def job (
    data : InferRequest,
    background_tasks : BackgroundTasks
):
    background_tasks.add_task(worker, data.text)
    return {"Status": "Checked"}