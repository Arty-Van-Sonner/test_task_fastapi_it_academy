from sqlalchemy import select
from models import NoteOrm
from database import new_session
from schemas import SNoteCreate, SNote, SNoteUpdate


class NoteRepository:
    @classmethod
    async def create_note(cls, note: SNoteCreate) -> NoteOrm:
        async with new_session() as session:
            note_dict = note.model_dump()

            note = NoteOrm(**note_dict)
            session.add(note)
            await session.flush()
            await session.commit()
            return note

    @classmethod
    async def get_all_notes(cls) -> list[NoteOrm]:
        async with new_session() as session:
            query = select(NoteOrm)
            result = await session.execute(query)
            note_models = result.scalars().all()
            return note_models
        
    @classmethod
    async def get_note_by_id(cls, note_id: int) -> NoteOrm | None: 
        async with new_session() as session:
            note_model = await session.get(NoteOrm, note_id)
            return note_model 
        
    @classmethod
    async def update_note(cls, note: NoteOrm, update_data: SNoteUpdate) -> NoteOrm | None:
        async with new_session() as session:
            update_data = update_data.model_dump(exclude_unset=True) 
            for key, value in update_data.items():
                setattr(note, key, value)
            session.add(note)
            await session.flush()
            await session.commit()
            return note
        
    @classmethod
    async def delete_note(cls, note: NoteOrm) -> bool:
        async with new_session() as session:
            await session.delete(note)
            await session.flush()
            await session.commit()
            return True