import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.bulletin import repository, schemas, services


@pytest.fixture
def repo(db_session: AsyncSession) -> repository.SqlalchemyPostRepository:
    return repository.SqlalchemyPostRepository(db_session)


async def test_create_post(repo: repository.SupportsPostRepository):
    got = await services.create_post(
        repo,
        username="testuser",
        title="hi",
        text="hello, world!",
    )
    want = schemas.PostSchema(
        id=1,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=got.created_at,
    )

    assert got == want


async def test_get_post(
    db_session: AsyncSession, repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await services.get_post(repo, id=1)
    want = schemas.PostSchema(
        id=1,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=got.created_at,
    )

    assert got == want


async def test_get_post_not_found(repo: repository.SupportsPostRepository):
    got = await services.get_post(repo, id=42)
    want = None

    assert got == want


async def test_get_posts(
    db_session: AsyncSession, repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES
        ('oldest_post', 'hello, oldest_post!', 'testuser', '2024-02-13 08:00'),
        ('newest_post', 'hello, newest_post!', 'testuser', '2024-02-15 12:00')
    ;
    """
    await db_session.execute(text(qry))

    got = await services.get_posts(repo)
    want = [
        schemas.PostSchema(
            id=2,
            title="newest_post",
            text="hello, newest_post!",
            created_by="testuser",
            created_at=datetime.datetime(2024, 2, 15, 12, 0),
        ),
        schemas.PostSchema(
            id=1,
            title="oldest_post",
            text="hello, oldest_post!",
            created_by="testuser",
            created_at=datetime.datetime(2024, 2, 13, 8, 0),
        ),
    ]

    assert got == want


async def test_get_all_none_found(repo: repository.SupportsPostRepository):
    got = await services.get_posts(repo)
    want = []

    assert got == want
