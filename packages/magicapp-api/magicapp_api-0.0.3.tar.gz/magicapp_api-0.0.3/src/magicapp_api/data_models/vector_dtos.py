from pydantic import BaseModel


class VectorMetadata(BaseModel):
    guideline_id: int = -1
    section_id: int = -1
    recommendation_id: int = -1
    pico_id: int = -1
    outcome_id: int = -1
    text: str
