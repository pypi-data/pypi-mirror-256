from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text

from poaster.core.tables import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(Text(), nullable=False)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
