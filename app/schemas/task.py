from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: int
    assigned_to: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    project_id: int
    assigned_to: int

    class Config:
        from_attributes = True