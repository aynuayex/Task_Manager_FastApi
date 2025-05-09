from fastapi import FastAPI, HTTPException, Path

from typing import List
from pydantic import BaseModel, Field

app = FastAPI()

# ----------------- Schemas for the Task Manager ------------------

class TaskModel(BaseModel):
    id: int = Field(gt=0 , default=1)
    title: str
    is_complete: bool = False 

class UpdateTask(BaseModel):
    title: str
    is_complete: bool

# =================================
task_list: List[TaskModel] = []

# add tasks for test
task_list.append(TaskModel(id=1, title="Task 1", is_complete=True))
task_list.append(TaskModel(id=2, title="Task 2", is_complete=False))
task_list.append(TaskModel(id=3, title="Task 3", is_complete=False))
task_list.append(TaskModel(id=4, title="Task 4", is_complete=False))

# =================================

@app.get("/tasks")
async def get_all_tasks():
    return task_list

@app.post("/tasks")
async def create_task(new_task: TaskModel):
    task_list.append(new_task)
    return { "detail": "Task Created!"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: int = Path(gt=0)):
    for task in task_list:
        if task.id == task_id:
            return task
    return HTTPException(status_code=404, detail="Task not Found!")

@app.put("/tasks/{task_id}")
async def update_task( updated_task: UpdateTask, task_id: int = Path(gt=0)):
    for task in task_list:
        if task.id == task_id:
            task.title = updated_task.title
            task.is_complete = updated_task.is_complete
            return task
    return HTTPException(status_code=404, detail="Task not Found!")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int = Path(gt=0)):
    for task in task_list:
        if task.id == task_id:
            task_list.remove(task)
            return { "detail": f"Task for id={task_id} removed!"}
    return HTTPException(status_code=404, detail="Task not Found!")
