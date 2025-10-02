import asyncio
from pydantic import BaseModel

class SNoteCreate(BaseModel):
    title: str | None
    body: str
    
class SNote(SNoteCreate):
    id: int

class SNoteUpdate(SNoteCreate):
    pass

class SNoutDelete(BaseModel):
    id: int
    detail: str = 'delete'
