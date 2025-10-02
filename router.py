from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query

from repository import NoteRepository
from schemas import SNoteCreate, SNote, SNoteDelete, SNoteUpdate, SNoteDelete

router = APIRouter(
    tags=['Notes'],
)

create_update_example = {
    'title': 'Important note',
    'body': 'When I leave, I need to turn off the iron',
}

note_not_found_example = {
    'detail': 'Note not found',
}

note_not_found_response = {
    'description': 'Note not found',
    'content': {
        'application/json': {
            'example': note_not_found_example,
        },
    },
}

success_create_response = {
    'description': 'Note created',
    'content': {
        'application/json': {
            'example': {
                'id': 3,
                'title': 'Important note',
                'body': 'When I leave, I need to turn off the iron'
            },
        },
    },
}

title_id_note = 'ID note in database'

async def get_note_by_id(note_id):
    note = await NoteRepository.get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail='Note not found')
    return note

@router.get('/notes')
async def get_notes() -> list[SNote]:
    notes = await NoteRepository.get_all_notes()
    return list(map(lambda note: SNote(**note.to_dict()), notes))

@router.get('/notes/{note_id}', responses={404: note_not_found_response,})
async def get_note(note_id: Annotated[int, Path(..., title=title_id_note)]) -> SNote:
    note = await get_note_by_id(note_id)
    return SNote(**note.to_dict())

@router.post('/notes', status_code=201, responses={201: success_create_response})
async def create_note(
    note: Annotated[SNoteCreate, Body(..., example=create_update_example)],
) -> SNote:
    note = await NoteRepository.create_note(note)
    return SNote(**note.to_dict())

@router.put('/notes/{note_id}/update', responses={404: note_not_found_response,})
async def update_note(
    note_id: Annotated[int, Path(..., title=title_id_note)], 
    update_data: Annotated[SNoteUpdate, Body(..., example=create_update_example)]
) -> SNote:
    note = await get_note_by_id(note_id)
    note = await NoteRepository.update_note(note, update_data)
    return SNote(**note.to_dict())

@router.delete('/notes/{note_id}/delete', responses={404: note_not_found_response,})
async def delete_note(
    note_id: Annotated[int, Path(..., title=title_id_note)], 
) -> SNoteDelete:
    note = await get_note_by_id(note_id)
    note = await NoteRepository.delete_note(note)
    return SNoteDelete(id=note_id, detail='Note deleted')
