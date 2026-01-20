from pydantic import BaseModel

class AttemptCreate(BaseModel):
    user_id: int
    passage_id: int

    wpm: int
    accuracy_score: float
    fluency_score: float

    mispronounced_count: int = 0
    skipped_count: int = 0
    stutter_count: int = 0
