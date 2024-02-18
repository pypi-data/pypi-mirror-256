from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from poaster.core import exceptions

from . import schemas, tables


class SupportsPostRepository(Protocol):
    """Interface for handling posts."""

    async def create(self, post: schemas.PostWithUsernameSchema) -> schemas.PostSchema:
        """Create post after validating input schema."""
        ...

    async def get_all(self) -> list[schemas.PostSchema]:
        """Fetch all posts from the DB."""
        ...

    async def get_by_id(self, id: int) -> schemas.PostSchema:
        """Fetch by id, raising exception if not found."""
        ...


class SqlalchemyPostRepository:
    """Implementation of the post repository with SqlAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, post: schemas.PostWithUsernameSchema) -> schemas.PostSchema:
        entry = tables.Post(
            **post.model_dump(exclude={"username"}),
            created_by=post.username,
        )

        self._session.add(entry)
        await self._session.commit()

        return schemas.PostSchema.model_validate(entry)

    async def get_all(self) -> list[schemas.PostSchema]:
        qry = select(tables.Post).order_by(tables.Post.created_at.desc())
        results = await self._session.execute(qry)
        return [schemas.PostSchema.model_validate(res) for res in results.scalars()]

    async def get_by_id(self, id: int) -> schemas.PostSchema:
        if (post := await self._session.get(tables.Post, id)) is None:
            raise exceptions.DoesNotExist("Post doesn't exist.")

        return schemas.PostSchema.model_validate(post)
