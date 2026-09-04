from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel

from task import celery_app, worker


app = FastAPI()


class InferRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {
        "status": "alive"
    }


@app.post("/infer", status_code=202)
def infer(data: InferRequest):

    task = worker.delay(data.text)

    return {
        "status": "queued",
        "task_id": task.id
    }


@app.get("/result/{task_id}")
def get_result(task_id: str):

    task = AsyncResult(
        task_id,
        app=celery_app
    )

    if task.successful():
        return {
            "status": task.status,
            "result": task.result
        }

    if task.failed():
        return {
            "status": task.status,
            "error": str(task.result)
        }

    return {
        "status": task.status,
        "result": None
    }