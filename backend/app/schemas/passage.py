from pydantic import BaseModel, Field

class PassageCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10)
    difficulty_level: str = Field(..., max_length=50)
