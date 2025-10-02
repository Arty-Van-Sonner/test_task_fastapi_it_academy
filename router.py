from typing import Annotated
from fastapi import APIRouter, Body, Depends

from repository import NoteRepository
from schemas import SNoteCreate, SNote, SNoteUpdate, SNoutDelete

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks'],
)

@router.post('/notes')
async def create_task(
    note: Annotated[SNoteCreate, Body(..., example={
            'title': 'Important note',
            'body': 'When I leave, I need to turn off the iron'
        })],
) -> SNote:
    note = await NoteRepository.create_note(note)
    return SNote(**note.model_dump())

@router.get('/notes')
async def get_tasks() -> list[SNote]:
    notes = await NoteRepository.get_all_notes()
    return list(map(lambda note: SNote.model_validate(note.to_dict()), notes))