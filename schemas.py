import asyncio
from pydantic import BaseModel

class SNote(BaseModel):
    id: int
    title: str | None
    body: str

class SNoteCreate(BaseModel):
    title: str | None
    body: str

class SNoteUpdate(SNoteCreate):
    pass

class SNoteDelete(BaseModel):
    id: int
    detail: str = 'Note deleted'
