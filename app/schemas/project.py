from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int 

    class Config:
        from_attributes = True