
# API	Purpose
# POST /tasks	Task create
# GET /tasks	All tasks
# GET /tasks/{id}	Task detail
# GET /tasks/my	Logged-in user tasks
# PUT /tasks/{id}	Update task
# PATCH /tasks/{id}/status	Update status
# PATCH /tasks/{id}/assign	Reassign
# DELETE /tasks/{id}	Delete
# GET /tasks?filters	Filtering
# GET /tasks/{id}/activity	Audit log



from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.schemas.task_schema import TaskCreate
from app.models.user import User
from datetime import datetime


def create_task(db:Session, data:TaskCreate ,current_user:int)->Task:

    if not data.title:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="task title is required")
    
    if not data.assigned_to_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="assigned user id is required")
    
    assigned_user = db.query(User).filter(User.id == data.assigned_to_id).first()
    if not assigned_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="assigned user not found")

    new_task= Task(
        title= data.title,
        description= data.description,
        assigned_to_id= data.assigned_to_id,
        created_by_id =current_user,
        status="pending",
        priority=data.priority or "medium",
        due_date= data.due_date,
        created_at = datetime.utcnow()
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task