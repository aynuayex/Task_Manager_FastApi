from fastapi import FastAPI, HTTPException

from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field

app = FastAPI()

# ----------------- Schemas for the Task Manager ------------------

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TaskBase(BaseModel):
    title: str =  Field(..., min_length=3, max_length=512, description="Title of the task")
    description: str = Field(..., description="Description of the task")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the task")
    is_complete: bool = False 

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int = Field(..., description="unique identifier of the task") 

class TaskUpdate(BaseModel):
    title: Optional[str] =  Field(None, min_length=3, max_length=512, description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    priority: Optional[Priority] = Field(None, description="Priority of the task")
    is_complete: Optional[bool] = None 

# =================================
task_list: List[Task] = []

# add tasks for test
task_list.append(Task(id=1, title="Task 1", description="This is Task 1", priority=Priority.LOW, is_complete=True))
task_list.append(Task(id=2, title="Task 2", description="This is Task 2", priority=Priority.HIGH,  is_complete=False))
task_list.append(Task(id=3, title="Task 3", description="This is Task 3", priority=Priority.LOW,  is_complete=False))
task_list.append(Task(id=4, title="Task 4", description="This is Task 4", priority=Priority.MEDIUM,  is_complete=True))

# =================================

@app.get("/tasks", response_model=List[Task])
async def get_all_tasks(first_n: int = None):
    if first_n:
        return task_list[:first_n]
    return task_list


@app.post("/tasks", response_model=Task)
async def create_task(new_task: TaskCreate):
    new_task_id = max(task.id for task in task_list) + 1
    new_task = Task(id = new_task_id, title = new_task.title, description = new_task.description, priority=new_task.priority)

    task_list.append(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in task_list:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not Found!")


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task( task_id: int, updated_task: TaskUpdate):
    for task in task_list:
        if task.id == task_id:
            if updated_task.title:
                task.title = updated_task.title
            if updated_task.description:
                task.description = updated_task.description
            if updated_task.is_complete:
                task.is_complete = updated_task.is_complete
            if updated_task.priority:
                task.priority = updated_task.priority

            return task
    raise HTTPException(status_code=404, detail="Task not Found!")


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for task in task_list:
        if task.id == task_id:
            task_list.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not Found!")
