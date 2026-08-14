from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)