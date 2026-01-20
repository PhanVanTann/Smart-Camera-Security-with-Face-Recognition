from pydantic import BaseModel
from typing import List, Optional

class FaceEmbedding(BaseModel):
    vector: List[float]
    angle: Optional[str] = None       
    mask: Optional[bool] = None       
    distance: Optional[str] = None 
class ResidentCreate(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int]
    address: Optional[str]
    embeddings: Optional[List[FaceEmbedding]] = []

