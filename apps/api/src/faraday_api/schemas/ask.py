"""POST /ask request shape."""
from pydantic import BaseModel
from pydantic import Field


class AskRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
