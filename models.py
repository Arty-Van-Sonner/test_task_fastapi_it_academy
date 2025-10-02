from database import Model
from sqlalchemy.orm import Mapped, mapped_column

class NoteOrm(Model):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None]
    body: Mapped[str]

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }