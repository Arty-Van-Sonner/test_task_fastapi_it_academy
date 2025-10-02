from sqlalchemy import select
from models import NoteOrm
from database import new_session
from schemas import SNoteCreate, SNote


class NoteRepository:
    @classmethod
    async def create_note(cls, task: SNoteCreate) -> NoteOrm:
        async with new_session() as session:
            task_dict = task.model_dump()

            task = NoteOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task


    @classmethod
    async def get_all_notes(cls) -> list[NoteOrm]:
        async with new_session() as session:
            query = select(NoteOrm)
            result = await session.execute(query)
            note_models = result.scalars().all()
            return note_models