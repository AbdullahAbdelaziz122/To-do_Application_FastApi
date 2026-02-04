from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Simple Todo API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (list)
tasks_db = []

# Models
class Task(BaseModel):
    id: str
    text: str
    completed: bool = False

class TaskCreate(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Todo API is running", "endpoints": ["GET /tasks", "POST /tasks", "DELETE /tasks/{id}"]}

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """Get all tasks"""
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskCreate):
    """Create a new task"""
    task_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
    new_task = Task(id=task_id, text=task_data.text)
    tasks_db.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete a task by ID"""
    global tasks_db
    initial_length = len(tasks_db)
    tasks_db = [task for task in tasks_db if task.id != task_id]
    
    if len(tasks_db) == initial_length:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully", "id": task_id}

@app.delete("/tasks")
def delete_all_tasks():
    """Delete all tasks"""
    global tasks_db
    tasks_db.clear()
    return {"message": "All tasks deleted successfully"}