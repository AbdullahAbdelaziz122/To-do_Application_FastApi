from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import uuid
import os

# MongoDB connection
try:
    MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
    
    from motor.motor_asyncio import AsyncIOMotorClient  
    
    client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    db = client.todoapp
    todos_collection = db.todos
    
    print("Successfully connected to MongoDB")
except ImportError:
    print("Motor not installed. Please install motor: pip install motor")
    raise
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

app = FastAPI(
    title="Todo API with MongoDB",
    description="A simple todo list API with MongoDB persistence",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TaskCreate(BaseModel):
    text: str
    completed: bool = False

class TaskUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: str
    text: str
    completed: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

# Helper function to convert MongoDB document to response model
def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "text": task["text"],
        "completed": task.get("completed", False),
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at")
    }

@app.get("/", response_model=dict)
async def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Todo API is running with MongoDB",
        "endpoints": {
            "GET /": "This message",
            "GET /health": "Health check",
            "GET /tasks": "Get all tasks",
            "POST /tasks": "Create a new task",
            "DELETE /tasks/{id}": "Delete a task by ID",
            "DELETE /tasks": "Delete all tasks"
        }
    }

@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    try:
        # Try to ping MongoDB
        await client.admin.command('ping')
        db_status = "connected"
        
        # Get tasks count
        tasks_count = await todos_collection.count_documents({})
        
        return {
            "status": "healthy",
            "mongodb": db_status,
            "tasks_count": tasks_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB connection error: {str(e)}"
        )

@app.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks():
    """Get all tasks from MongoDB"""
    try:
        tasks = []
        async for task in todos_collection.find().sort("created_at", -1):  # Sort by newest first
            tasks.append(task_helper(task))
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tasks: {str(e)}"
        )

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    """Create a new task in MongoDB"""
    try:
        # Create task document
        task_doc = {
            "text": task_data.text,
            "completed": task_data.completed,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = await todos_collection.insert_one(task_doc)
        
        # Get the inserted document
        inserted_task = await todos_collection.find_one({"_id": result.inserted_id})
        
        if not inserted_task:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create task"
            )
        
        return task_helper(inserted_task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    """Delete a task by ID from MongoDB"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format"
            )
        
        # Delete task
        result = await todos_collection.delete_one({"_id": ObjectId(task_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return {
            "message": "Task deleted successfully",
            "id": task_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )

@app.delete("/tasks", response_model=dict)
async def delete_all_tasks():
    """Delete all tasks from MongoDB"""
    try:
        # Get count before deletion
        count = await todos_collection.count_documents({})
        
        # Delete all tasks
        result = await todos_collection.delete_many({})
        
        return {
            "message": "All tasks deleted successfully",
            "deleted_count": result.deleted_count,
            "previous_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting all tasks: {str(e)}"
        )

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Update a task (optional endpoint for completeness)"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format"
            )
        
        # Prepare update data
        update_data = {"updated_at": datetime.utcnow()}
        if task_data.text is not None:
            update_data["text"] = task_data.text
        if task_data.completed is not None:
            update_data["completed"] = task_data.completed
        
        # Update task
        result = await todos_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Get updated task
        updated_task = await todos_collection.find_one({"_id": ObjectId(task_id)})
        
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve updated task"
            )
        
        return task_helper(updated_task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )