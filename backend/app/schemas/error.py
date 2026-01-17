from pydantic import BaseModel
from typing import Optional

class ErrorCreate(BaseModel):
    attempt_id: int
    error_type: str
    word_expected: Optional[str] = None
    word_spoken: Optional[str] = None
